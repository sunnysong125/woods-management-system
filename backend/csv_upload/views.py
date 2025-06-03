from django.shortcuts import render
import csv
from io import StringIO
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction

from .models import CSVFile, DataRecord
from .serializers import CSVFileSerializer, DataRecordSerializer, DataRecordCreateSerializer
from users.views import IsAdminUser

class IsOwnerOrAdmin(permissions.BasePermission):
    """只允许创建者或管理员访问"""
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有对象
        if request.user.is_admin:
            return True
        # 创建者可以访问自己的对象
        return obj.user == request.user

class CSVFileViewSet(viewsets.ModelViewSet):
    """CSV文件管理视图集"""
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 管理员可以看到所有文件，普通用户只能看到自己的文件
        if self.request.user.is_admin:
            return CSVFile.objects.all()
        return CSVFile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def process_csv(self, request, pk=None):
        """处理CSV文件并创建数据记录"""
        csv_file_obj = self.get_object()
        
        if csv_file_obj.processed:
            return Response({'message': '此CSV文件已经处理过'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 读取CSV文件
            file_content = csv_file_obj.file.read().decode('utf-8')
            csv_reader = csv.reader(StringIO(file_content))
            
            # 跳过表头
            next(csv_reader, None)
            
            # 批量创建数据记录
            with transaction.atomic():
                records = []
                for row in csv_reader:
                    if len(row) >= 5:  # 确保行至少有5个字段
                        record = DataRecord(
                            csv_file=csv_file_obj,
                            field1=row[0],
                            field2=row[1],
                            field3=row[2],
                            field4=row[3],
                            field5=row[4]
                        )
                        records.append(record)
                
                DataRecord.objects.bulk_create(records)
                csv_file_obj.processed = True
                csv_file_obj.save()
            
            return Response({
                'message': f'成功处理CSV文件，创建了{len(records)}条记录',
                'records_count': len(records)
            })
            
        except Exception as e:
            return Response({'message': f'处理CSV文件时出错: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class DataRecordViewSet(viewsets.ModelViewSet):
    """数据记录管理视图集"""
    queryset = DataRecord.objects.all()
    serializer_class = DataRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 管理员可以看到所有记录，普通用户只能看到自己的CSV文件的记录
        if self.request.user.is_admin:
            return DataRecord.objects.all()
        return DataRecord.objects.filter(csv_file__user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DataRecordCreateSerializer
        return DataRecordSerializer
