# 樹木管理系統

這是一個用於管理樹木資料的完整系統，包含前端和後端部分。

## 主要功能

1. **樹木資料管理**
   - 新增、修改、刪除樹木記錄
   - 記錄樹木的基本資訊（樹種、胸徑、樹高等）
   - 支援專案分類管理

2. **歷史記錄追蹤**
   - 自動記錄樹木資料的變更歷史
   - 可查看每棵樹的完整變更記錄
   - 支援時間軸方式展示歷史資料

3. **QR 碼生成**
   - 支援單一樹木 QR 碼生成
   - 支援批量生成 QR 碼
   - QR 碼包含樹木基本資訊

4. **圖片管理**
   - 支援上傳樹木圖片
   - 圖片預覽功能
   - 圖片與樹木記錄關聯

5. **權限管理**
   - 管理員與一般使用者權限區分
   - 敏感操作需要管理員權限

## 技術架構

- 前端：Vue.js + Element Plus
- 後端：Django + Django REST framework
- 資料庫：PostgreSQL
- 圖片儲存：本地檔案系統

## 目錄結構

```
woods/
├── backend/          # Django 後端專案
├── frontend/         # Vue.js 前端專案
└── README.md         # 本文件
```

## 詳細說明

- 前端詳細說明請參考 `frontend/README.md`
- 後端詳細說明請參考 `backend/README.md`

## 安裝與運行

1. 安裝依賴
   ```bash
   # 後端依賴
   cd backend
   pip install -r requirements.txt

   # 前端依賴
   cd frontend
   npm install
   ```

2. 運行服務
   ```bash
   # 後端服務
   cd backend
   python manage.py runserver

   # 前端服務
   cd frontend
   npm run serve
   ```

3. 訪問系統
   - 前端：http://localhost:8080
   - 後端 API：http://localhost:8000/api/