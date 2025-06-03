from rest_framework import viewsets, permissions, status
from .models import Tree, TreeImage, Project, TreeHistory
from .serializers import TreeSerializer, TreeImageSerializer, ProjectSerializer, TreeHistorySerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import csv
from io import StringIO
from django.db import transaction
import datetime
from rest_framework.permissions import AllowAny, IsAdminUser
import qrcode
import os
import json
from django.conf import settings
import io
import zipfile
from django.http import HttpResponse
from django.core.files.base import ContentFile
from PIL import Image

class ProjectViewSet(viewsets.ModelViewSet):
    """
    專案數據的API視圖集
    提供 `list`, `create`, `retrieve`, `update` 和 `destroy` 操作
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        """
        根據操作類型設定不同的權限
        - list, retrieve: 所有人都可以檢視
        - create, update: 需要登入
        - destroy: 只有超級管理者或專案創建者可以刪除
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated]  # 修改為需要登入，具體權限在 check_object_permissions 中檢查
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """創建專案時自動設置創建者"""
        serializer.save(created_by=self.request.user)
    
    def check_object_permissions(self, request, obj):
        """檢查物件層級的權限"""
        super().check_object_permissions(request, obj)
        
        # 對於刪除操作，只有超級管理者或專案創建者可以執行
        if self.action == 'destroy':
            # 檢查是否為超級用戶
            is_superuser = request.user.is_superuser
            # 檢查是否為管理員
            is_admin = (request.user.is_staff or 
                       (hasattr(request.user, 'is_admin') and request.user.is_admin) or
                       getattr(request.user, 'role', None) == 'ADMIN')
            # 檢查是否為專案創建者
            is_creator = obj.created_by == request.user
            
            if not (is_superuser or is_admin or is_creator):
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("您沒有權限刪除此專案。只有超級管理者或專案創建者可以刪除專案。")

class TreeViewSet(viewsets.ModelViewSet):
    """
    樹木數據的API視圖集
    提供 `list`, `create`, `retrieve`, `update` 和 `destroy` 操作
    """
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        """獲取樹木列表"""
        queryset = Tree.objects.all().order_by('-created_at')
        
        # 處理請求查詢參數
        request = self.request
        if hasattr(request, 'query_params') and request.query_params:
            print(f"查詢參數: {dict(request.query_params)}")
            
            # 特別處理一些特定參數
            if 'project__name' in request.query_params:
                project_name = request.query_params.get('project__name')
                project = Project.objects.filter(name__icontains=project_name).first()
                if project:
                    queryset = queryset.filter(project_id=project.id)
                print(f"按專案名稱過濾: {project_name}")
            
            if 'diameter__gt' in request.query_params:
                try:
                    value = float(request.query_params.get('diameter__gt'))
                    queryset = queryset.filter(diameter__gt=value)
                    print(f"按胸徑大於過濾: > {value}")
                except (ValueError, TypeError):
                    print(f"無效的胸徑值: {request.query_params.get('diameter__gt')}")
            
            if 'diameter__lt' in request.query_params:
                try:
                    value = float(request.query_params.get('diameter__lt'))
                    queryset = queryset.filter(diameter__lt=value)
                    print(f"按胸徑小於過濾: < {value}")
                except (ValueError, TypeError):
                    print(f"無效的胸徑值: {request.query_params.get('diameter__lt')}")
            
            if 'height__gt' in request.query_params:
                try:
                    value = float(request.query_params.get('height__gt'))
                    queryset = queryset.filter(height__gt=value)
                    print(f"按樹高大於過濾: > {value}")
                except (ValueError, TypeError):
                    print(f"無效的樹高值: {request.query_params.get('height__gt')}")
            
            if 'height__lt' in request.query_params:
                try:
                    value = float(request.query_params.get('height__lt'))
                    queryset = queryset.filter(height__lt=value)
                    print(f"按樹高小於過濾: < {value}")
                except (ValueError, TypeError):
                    print(f"無效的樹高值: {request.query_params.get('height__lt')}")
            
            # 處理其他通用查詢參數
            for param, value in request.query_params.items():
                # 跳過已處理的特殊參數
                if param in ['project__name', 'diameter__gt', 'diameter__lt', 'height__gt', 'height__lt']:
                    continue
                
                # 處理其他條件
                if param == 'species__contains' and value:
                    queryset = queryset.filter(species__icontains=value)
                elif param == 'notes__contains' and value:
                    queryset = queryset.filter(notes__icontains=value)
                elif param == '_id' and value:
                    try:
                        id_value = int(value)
                        queryset = queryset.filter(_id=id_value)
                    except (ValueError, TypeError):
                        pass
            
            print(f"最終查詢結果數: {queryset.count()}")
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()
        
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        """上傳CSV文件並導入樹木數據"""
        print("進入upload_csv方法")  # 添加日誌
        if 'file' not in request.FILES:
            print("請求中缺少文件")  # 添加日誌
            return Response({'error': '請選擇CSV文件'}, status=status.HTTP_400_BAD_REQUEST)
            
        csv_file = request.FILES['file']
        print(f"接收到文件: {csv_file.name}")  # 添加日誌
        
        # 獲取專案ID和使用者ID
        project_id = request.data.get('project_id')
        user_id = request.data.get('user_id')
        batch_id = request.data.get('batch_id')  # 新增：獲取批次ID參數
        
        print(f"專案ID: {project_id}, 使用者ID: {user_id}, 批次ID: {batch_id}")  # 添加日誌
        
        # 檢查批次ID是否有效
        if batch_id:
            print(f"使用批次ID: {batch_id}")
        else:
            # 檢查是否為驗證模式或準備解析CSV以檢查ID欄位
            if not request.data.get('validate_only'):
                print("沒有提供批次ID，將檢查CSV文件是否包含ID欄位")
                # 不立即返回錯誤，而是在後續解析CSV時檢查
        
        # 檢查專案ID是否有效
        if project_id:
            try:
                project_id = int(project_id)
                # 確認專案存在
                if not Project.objects.filter(id=project_id).exists():
                    return Response({'error': f'專案ID {project_id} 不存在'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': '專案ID必須是數字'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查文件類型
        if not csv_file.name.endswith('.csv'):
            print("文件類型不正確")  # 添加日誌
            return Response({'error': '只接受CSV文件'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 讀取CSV文件
            decoded_file = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(StringIO(decoded_file))
            
            # 檢查CSV欄位是否包含必要欄位
            required_fields = ['species', 'diameter', 'height', 'record_date']
            headers = csv_reader.fieldnames
            
            if not headers:
                return Response({'error': 'CSV文件為空或格式不正確'}, status=status.HTTP_400_BAD_REQUEST)
            
            missing_fields = [field for field in required_fields if field not in headers]
            if missing_fields:
                return Response({
                    'valid': False,
                    'errors': [f'缺少必要欄位: {", ".join(missing_fields)}']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 驗證模式，只檢查不導入
            validate_only = request.data.get('validate_only', 'false').lower() == 'true'
            print(f"驗證模式: {validate_only}")
            
            errors = []
            valid_rows = []
            row_number = 0
            
            # 讀取CSV，進行驗證
            for row in csv.DictReader(StringIO(decoded_file)):
                row_number += 1
                row_errors = []
                
                # 檢查ID欄位
                has_row_id = 'ID' in row or 'id' in row
                row_id = row.get('ID') or row.get('id')
                
                # 如果CSV中沒有ID且沒有設置批次ID，報錯
                if not has_row_id and not batch_id and not validate_only:
                    row_errors.append(f"第{row_number}行缺少ID欄位，且未設置批次ID")
                
                # 檢查必填欄位
                if not row.get('species'):
                    row_errors.append(f"第{row_number}行缺少樹種名稱")
                    
                # 驗證數值欄位
                try:
                    if row.get('diameter'):
                        float(row['diameter'])
                except ValueError:
                    row_errors.append(f"第{row_number}行的樹徑不是有效的數字")
                
                try:
                    if row.get('height'):
                        float(row['height'])
                except ValueError:
                    row_errors.append(f"第{row_number}行的樹高不是有效的數字")
                
                # 驗證日期格式
                if row.get('record_date'):
                    try:
                        datetime.datetime.strptime(row['record_date'], '%Y-%m-%d')
                    except ValueError:
                        row_errors.append(f"第{row_number}行的日期格式無效，應為YYYY-MM-DD")
                
                # 收集錯誤並保存有效行
                if row_errors:
                    errors.extend(row_errors)
                else:
                    valid_rows.append(row)
            
            # 只驗證模式下，返回驗證結果
            if validate_only:
                return Response({
                    'valid': len(errors) == 0,
                    'errors': errors,
                    'valid_count': len(valid_rows),
                    'total_count': row_number
                })
            
            # 如果有錯誤，返回錯誤信息
            if errors:
                return Response({
                    'valid': False,
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 導入數據
            count = 0
            import_errors = []
            
            with transaction.atomic():
                for row in valid_rows:
                    try:
                        # 處理日期
                        record_date = None
                        if row.get('record_date'):
                            record_date = datetime.datetime.strptime(row['record_date'], '%Y-%m-%d').date()
                        
                        # 處理數值字段
                        diameter = float(row.get('diameter', 0)) if row.get('diameter') else None
                        height = float(row.get('height', 0)) if row.get('height') else None
                        
                        # 使用傳入的專案ID，如果CSV中有指定則優先使用CSV中的
                        row_project_id = None
                        if row.get('project_id'):
                            try:
                                row_project_id = int(row['project_id'])
                            except ValueError:
                                import_errors.append(f"第{count+1}行的專案ID不是有效的數字")
                                continue
                        
                        final_project_id = row_project_id or project_id
                        
                        # 獲取樹木ID
                        tree_id = None
                        if 'ID' in row or 'id' in row:
                            try:
                                tree_id = int(row.get('ID') or row.get('id'))
                                print(f"從CSV獲取到樹木ID: {tree_id}")
                            except ValueError:
                                import_errors.append(f"第{count+1}行的ID不是有效的數字")
                                continue
                        elif batch_id:
                            # 使用批次ID
                            tree_id = int(batch_id)
                            print(f"使用批次ID: {tree_id}")
                        else:
                            # 既沒有CSV中的ID，也沒有批次ID
                            import_errors.append(f"第{count+1}行缺少ID，且未設置批次ID")
                            continue
                        
                        # 檢查是否存在相同ID的樹木
                        existing_tree = None
                        try:
                            existing_tree = Tree.objects.get(_id=tree_id)
                        except Tree.DoesNotExist:
                            pass
                        
                        # 如果存在相同ID的樹木，將其保存到歷史記錄中
                        if existing_tree:
                            print(f"發現現有樹木ID={tree_id}，保存到歷史記錄")
                            TreeHistory.objects.create(
                                tree_id=existing_tree._id,
                                action='UPDATE',
                                species=existing_tree.species,
                                diameter=existing_tree.diameter,
                                height=existing_tree.height,
                                record_date=existing_tree.record_date,
                                project=existing_tree.project,
                                notes=existing_tree.notes
                            )
                            
                            # 更新現有樹木
                            existing_tree.species = row.get('species', '')
                            existing_tree.diameter = diameter
                            existing_tree.height = height
                            existing_tree.record_date = record_date
                            existing_tree.project_id = final_project_id
                            existing_tree.notes = row.get('notes', '')
                            
                            # 如果有使用者ID，設定created_by
                            if user_id:
                                from django.contrib.auth import get_user_model
                                User = get_user_model()
                                try:
                                    user_id_int = int(user_id)
                                    user = User.objects.get(id=user_id_int)
                                    existing_tree.created_by = user
                                except (ValueError, User.DoesNotExist):
                                    pass
                            
                            existing_tree.save()
                            print(f"更新樹木ID={existing_tree._id}")
                        else:
                            # 創建新樹木記錄
                            tree = Tree(
                                _id=tree_id,
                                species=row.get('species', ''),
                                diameter=diameter,
                                height=height,
                                record_date=record_date,
                                project_id=final_project_id,
                                notes=row.get('notes', '')
                            )
                            
                            # 如果有使用者ID，設定created_by
                            if user_id:
                                from django.contrib.auth import get_user_model
                                User = get_user_model()
                                try:
                                    user_id_int = int(user_id)
                                    user = User.objects.get(id=user_id_int)
                                    tree.created_by = user
                                except (ValueError, User.DoesNotExist):
                                    pass
                            
                            tree.save()
                            print(f"新建樹木ID={tree._id}")
                        
                        count += 1
                        
                    except Exception as e:
                        print(f"處理第{count+1}行時出錯: {str(e)}")
                        import_errors.append(f"第{count+1}行處理錯誤: {str(e)}")
            
            # 返回導入結果
            response_data = {
                'success': True,
                'count': count,
                'total': len(valid_rows),
                'message': f'成功導入{count}條樹木記錄'
            }
            
            if import_errors:
                response_data['success'] = False
                response_data['errors'] = import_errors
            
            return Response(response_data)
            
        except Exception as e:
            print(f"處理CSV文件時發生錯誤: {str(e)}")
            return Response({
                'error': f'處理CSV文件時發生錯誤: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='test')
    def test(self, request):
        """測試API是否能正常訪問"""
        print("測試端點被訪問")
        return Response({'message': '測試成功！API正常工作'}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'], url_path='generate-bulk-qr')
    def generate_bulk_qr(self, request):
        """批量生成樹木QR碼並提供下載"""
        if not request.user.is_staff:
            return Response({'error': '只有管理員可以生成QR碼'}, status=status.HTTP_403_FORBIDDEN)

        tree_ids = request.data.get('tree_ids', [])
        if not tree_ids:
            return Response({'error': '請提供樹木ID列表'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 創建一個內存中的zip文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                success_count = 0
                error_count = 0
                
                for tree_id in tree_ids:
                    try:
                        print(f'正在處理樹木 ID: {tree_id}')
                        tree = self.get_queryset().get(_id=tree_id)
                        
                        # 獲取樹木的最近一筆歷史資料
                        latest_history = None
                        try:
                            latest_history = TreeHistory.objects.filter(tree_id=tree_id).order_by('-created_at').first()
                            print(f'找到最近的歷史記錄: {latest_history.id if latest_history else "無"}')
                        except Exception as hist_err:
                            print(f'獲取歷史記錄時出錯: {str(hist_err)}')
                        
                        # 準備QR碼數據
                        qr_data = {
                            '_id': tree._id,
                            'species': tree.species,
                            'diameter': float(tree.diameter) if tree.diameter else None,
                            'height': float(tree.height) if tree.height else None,
                            'record_date': tree.record_date.strftime('%Y-%m-%d') if tree.record_date else None,
                            'project': tree.project.name if tree.project else None,
                            'notes': tree.notes,
                            'created_by': tree.created_by.username if tree.created_by else None
                        }
                        
                        # 添加最近一筆歷史資料
                        if latest_history:
                            qr_data['last_history'] = {
                                'action': latest_history.action,
                                'date': latest_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                'species': latest_history.species,
                                'diameter': float(latest_history.diameter) if latest_history.diameter else None,
                                'height': float(latest_history.height) if latest_history.height else None,
                                'record_date': latest_history.record_date.strftime('%Y-%m-%d') if latest_history.record_date else None,
                                'notes': latest_history.notes
                            }
                        
                        print(f'QR碼數據: {qr_data}')
                        
                        # 生成QR碼
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(json.dumps(qr_data, ensure_ascii=False))
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")
                        
                        # 將QR碼保存到內存中
                        img_buffer = io.BytesIO()
                        qr_img.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        
                        # 將圖片添加到zip文件中
                        zip_file.writestr(f'qrcode_{tree._id}.png', img_buffer.getvalue())
                        success_count += 1
                        print(f'成功生成樹木 {tree._id} 的QR碼')
                        
                    except Tree.DoesNotExist:
                        print(f'找不到樹木 ID: {tree_id}')
                        error_count += 1
                        continue
                    except Exception as e:
                        print(f'生成樹木 {tree_id} 的QR碼時發生錯誤: {str(e)}')
                        error_count += 1
                        continue

            if success_count == 0:
                return Response({'error': '沒有成功生成任何QR碼'}, status=status.HTTP_400_BAD_REQUEST)

            # 準備響應
            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="tree_qrcodes.zip"'
            return response

        except Exception as e:
            print(f'生成QR碼時發生錯誤: {str(e)}')
            return Response({'error': f'生成QR碼時發生錯誤: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        instance = self.get_object()
        # 保存歷史記錄
        TreeHistory.objects.create(
            tree_id=instance._id,
            action='UPDATE',
            species=instance.species,
            diameter=instance.diameter,
            height=instance.height,
            record_date=instance.record_date,
            project=instance.project,
            notes=instance.notes
        )
        serializer.save()

    def perform_destroy(self, instance):
        # 保存歷史記錄
        TreeHistory.objects.create(
            tree_id=instance._id,
            action='DELETE',
            species=instance.species,
            diameter=instance.diameter,
            height=instance.height,
            record_date=instance.record_date,
            project=instance.project,
            notes=instance.notes
        )
        instance.delete()

    @action(detail=False, methods=['get'], url_path='history/(?P<tree_id>[^/.]+)')
    def get_tree_history(self, request, tree_id=None):
        """獲取樹木的歷史記錄"""
        try:
            histories = TreeHistory.objects.filter(tree_id=tree_id).order_by('-created_at')
            serializer = TreeHistorySerializer(histories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TreeImageViewSet(viewsets.ModelViewSet):
    """
    樹木圖片的API視圖集
    提供 `list`, `create`, `retrieve`, `update` 和 `destroy` 操作
    """
    queryset = TreeImage.objects.all()
    serializer_class = TreeImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def generate_qr_code(request, tree_id):
    try:
        tree = Tree.objects.get(_id=tree_id)
        
        # 獲取樹木的最近一筆歷史資料
        latest_history = None
        try:
            latest_history = TreeHistory.objects.filter(tree_id=tree_id).order_by('-created_at').first()
        except Exception as hist_err:
            print(f'獲取歷史記錄時出錯: {str(hist_err)}')
        
        # 创建 QR Code 数据
        qr_data = {
            '_id': tree._id,
            'species': tree.species,
            'diameter': float(tree.diameter) if tree.diameter else None,
            'height': float(tree.height) if tree.height else None,
            'record_date': tree.record_date.strftime('%Y-%m-%d') if tree.record_date else None,
            'project': tree.project.name if tree.project else None,
            'notes': tree.notes,
            'created_by': tree.created_by.username if tree.created_by else None
        }
        
        # 添加最近一筆歷史資料
        if latest_history:
            qr_data['last_history'] = {
                'action': latest_history.action,
                'date': latest_history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'species': latest_history.species,
                'diameter': float(latest_history.diameter) if latest_history.diameter else None,
                'height': float(latest_history.height) if latest_history.height else None,
                'record_date': latest_history.record_date.strftime('%Y-%m-%d') if latest_history.record_date else None,
                'notes': latest_history.notes
            }
        
        # 生成 QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data, ensure_ascii=False))
        qr.make(fit=True)
        
        # 创建图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 确保目录存在
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)
        
        # 保存图片
        img_path = os.path.join(qr_dir, f'tree_{tree_id}.png')
        img.save(img_path)
        
        return Response({
            'message': 'QR Code generated successfully',
            'qr_code_url': f'/media/qr_codes/tree_{tree_id}.png'
        })
    except Tree.DoesNotExist:
        return Response({'error': 'Tree not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500) 