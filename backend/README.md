# 樹木管理系統後端

## 技術棧

- Python 3.8+
- Django 4.2
- Django REST framework
- PostgreSQL
- Pillow (圖片處理)
- qrcode (QR 碼生成)

## 目錄結構

```
backend/
├── core/              # Django 專案核心設置
├── users/             # 用戶管理應用
├── trees/             # 樹木資料管理應用
│   ├── models.py      # 數據模型
│   ├── serializers.py # 序列化器
│   ├── views.py       # 視圖
│   └── urls.py        # URL 配置
└── requirements.txt   # Python 依賴
```

## 主要功能

### 1. 用戶管理
- 用戶註冊
- 用戶登錄/登出
- 權限控制
- JWT 認證

### 2. 樹木資料管理
- 樹木記錄 CRUD
- 資料驗證
- 關聯專案管理
- 歷史記錄追蹤

### 3. 圖片處理
- 圖片上傳
- 圖片儲存
- 圖片預覽
- 圖片刪除

### 4. QR 碼生成
- 單一 QR 碼生成
- 批量 QR 碼生成
- QR 碼儲存
- QR 碼下載

### 5. 歷史記錄
- 自動記錄變更
- 歷史資料查詢
- 變更類型標記
- 時間戳記錄

## API 端點

### 用戶相關
- POST /api/users/register/ - 用戶註冊
- POST /api/users/login/ - 用戶登錄
- POST /api/users/logout/ - 用戶登出
- GET /api/users/current-user/ - 獲取當前用戶信息

### 樹木相關
- GET /api/trees/ - 獲取樹木列表
- POST /api/trees/ - 創建新樹木
- GET /api/trees/{id}/ - 獲取樹木詳情
- PUT /api/trees/{id}/ - 更新樹木資訊
- DELETE /api/trees/{id}/ - 刪除樹木
- GET /api/trees/history/{id}/ - 獲取樹木歷史記錄

### QR 碼相關
- POST /api/trees/generate-qr/ - 生成單一 QR 碼
- POST /api/trees/generate-bulk-qr/ - 批量生成 QR 碼

## 數據模型

### Tree
- id: 主鍵
- species: 樹種
- diameter: 胸徑
- height: 樹高
- record_date: 記錄日期
- project: 關聯專案
- notes: 備註
- created_at: 創建時間
- updated_at: 更新時間

### TreeHistory
- id: 主鍵
- tree_id: 關聯樹木 ID
- action: 操作類型
- species: 樹種
- diameter: 胸徑
- height: 樹高
- record_date: 記錄日期
- project: 關聯專案
- notes: 備註
- created_at: 創建時間

### TreeImage
- id: 主鍵
- tree: 關聯樹木
- image: 圖片文件
- created_at: 創建時間

## 安裝與設置

1. 創建虛擬環境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 設置環境變量
創建 `.env` 文件：
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
SECRET_KEY=your_secret_key
```

4. 數據庫遷移
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 創建超級用戶
```bash
python manage.py createsuperuser
```

6. 運行開發服務器
```bash
python manage.py runserver
```

## 開發指南

### 代碼規範
- 遵循 PEP 8 規範
- 使用 Django 最佳實踐
- 編寫文檔字符串
- 使用類型提示

### 安全性
- 使用 JWT 認證
- 實現 CSRF 保護
- 數據驗證
- 權限控制

### 性能優化
- 數據庫索引
- 查詢優化
- 緩存策略
- 異步任務

## 部署說明

### 生產環境設置
1. 設置 DEBUG=False
2. 配置 ALLOWED_HOSTS
3. 設置靜態文件
4. 配置數據庫

### 使用 Gunicorn
```bash
gunicorn core.wsgi:application
```

### Nginx 配置
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location /static/ {
        alias /path/to/static/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 維護與監控

### 日誌記錄
- 訪問日誌
- 錯誤日誌
- 操作日誌
- 性能日誌

### 監控指標
- 響應時間
- 錯誤率
- 資源使用
- 數據庫性能

### 備份策略
- 定期數據庫備份
- 媒體文件備份
- 配置備份
- 恢復測試 