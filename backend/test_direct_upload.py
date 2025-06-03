import requests
import os

def test_csv_upload():
    """測試直接向API端點上傳CSV文件"""
    print("開始測試CSV上傳...")
    
    # 準備測試數據
    csv_content = """species,diameter,height,record_date,project_id,notes
台灣紅檜,120.5,25.7,2024-03-15,1,位於中部山區的古老紅檜，樹齡約300年"""
    
    # 創建臨時CSV文件
    temp_file_path = "temp_test.csv"
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    # 文件對象
    file_obj = None
    
    try:
        print(f"創建臨時文件: {temp_file_path}")
        
        # 準備表單數據（注意正確關閉文件）
        file_obj = open(temp_file_path, 'rb')
        files = {
            'file': ('test.csv', file_obj, 'text/csv')
        }
        
        # 發送POST請求
        url = "http://localhost:8000/api/trees/upload-csv/"
        print(f"發送請求到: {url}")
        
        # 由於API檢測需要身份驗證，我們必須修改一下views.py
        print("現在我們需要調整API設置來允許未認證的上傳...")
        
        # 顯示請求信息
        print("請求頭:")
        print("- Content-Type: multipart/form-data (由requests自動設置)")
        
        # 測試可能需要身份驗證
        response = requests.post(url, files=files)
        
        # 輸出響應信息
        print(f"\n響應狀態碼: {response.status_code}")
        print(f"響應頭: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"上傳成功!")
            try:
                print(f"響應數據: {response.json()}")
            except:
                print(f"響應內容: {response.text}")
        else:
            print(f"上傳失敗! 狀態碼: {response.status_code}")
            try:
                print(f"錯誤信息: {response.json()}")
            except:
                print(f"錯誤內容: {response.text}")
            
            if response.status_code == 401:
                print("\n需要對views.py進行修改，將permission_classes設為允許所有用戶。")
                print("請檢查woods/backend/trees/views.py文件，修改TreeViewSet類的permission_classes。")
    
    except Exception as e:
        print(f"測試過程中發生錯誤: {str(e)}")
    
    finally:
        # 確保文件被關閉
        if file_obj:
            file_obj.close()
            
        # 清理臨時文件
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print(f"已刪除臨時文件: {temp_file_path}")
        except Exception as e:
            print(f"刪除臨時文件時出錯: {str(e)}")
            print("您可能需要手動刪除temp_test.csv文件")

if __name__ == "__main__":
    test_csv_upload() 