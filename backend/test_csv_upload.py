import os
import django
import csv
import io
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from trees.models import Tree

def test_csv_processing():
    """測試CSV處理邏輯"""
    print("開始測試CSV處理...")
    
    # 創建測試CSV數據
    csv_data = """species,diameter,height,record_date,project_id,notes
台灣紅檜,120.5,25.7,2024-03-15,1,位於中部山區的古老紅檜，樹齡約300年
香杉,80.2,18.3,2024-03-16,1,山區常見的香杉，樹勢良好"""
    
    # 模擬文件對象
    csv_file = SimpleUploadedFile(
        name='test.csv',
        content=csv_data.encode('utf-8'),
        content_type='text/csv'
    )
    
    try:
        # 讀取CSV數據
        decoded_file = csv_file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(decoded_file))
        
        count = 0
        errors = []
        
        # 處理每一行數據
        for row in csv_reader:
            try:
                print(f"處理第{count+1}行: {row}")
                
                # 處理日期
                record_date = None
                if row.get('record_date'):
                    try:
                        record_date = datetime.datetime.strptime(row['record_date'], '%Y-%m-%d').date()
                    except ValueError:
                        errors.append(f"第{count+1}行的日期格式無效")
                        continue
                
                # 處理數值字段
                try:
                    diameter = float(row.get('diameter', 0)) if row.get('diameter') else None
                except ValueError:
                    diameter = None
                    errors.append(f"第{count+1}行的樹徑不是有效的數字")
                    
                try:
                    height = float(row.get('height', 0)) if row.get('height') else None
                except ValueError:
                    height = None
                    errors.append(f"第{count+1}行的樹高不是有效的數字")
                
                # 處理專案ID
                project_id = None
                if row.get('project_id'):
                    try:
                        project_id = int(row['project_id'])
                    except ValueError:
                        errors.append(f"第{count+1}行的專案ID不是有效的數字")
                        continue
                
                # 創建樹木對象（但不保存到數據庫）
                tree = Tree(
                    species=row.get('species', ''),
                    diameter=diameter,
                    height=height,
                    record_date=record_date,
                    project_id=project_id,
                    notes=row.get('notes', '')
                )
                
                print(f"成功處理樹木: ID={tree._id}, 樹種={tree.species}, 樹徑={tree.diameter}, 樹高={tree.height}")
                count += 1
                
            except Exception as e:
                print(f"處理第{count+1}行時出錯: {str(e)}")
                errors.append(f"第{count+1}行處理錯誤: {str(e)}")
        
        # 輸出處理結果
        print(f"\n處理完成，成功處理了{count}行")
        if errors:
            print("\n錯誤信息:")
            for error in errors:
                print(f"- {error}")
    
    except Exception as e:
        print(f"處理CSV文件時發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_csv_processing() 