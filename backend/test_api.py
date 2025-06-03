import requests

def test_api_endpoints():
    """測試API端點是否可訪問"""
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/",
        "/api/trees/",
        "/api/trees/test/",
    ]
    
    print("開始測試API端點...")
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\n測試端點: {url}")
        
        try:
            response = requests.get(url)
            print(f"狀態碼: {response.status_code}")
            print(f"響應內容: {response.text[:200]}...")
        except Exception as e:
            print(f"訪問失敗: {str(e)}")
    
    print("\n測試完成。")

if __name__ == "__main__":
    test_api_endpoints() 