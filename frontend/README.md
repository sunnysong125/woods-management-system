# 樹木管理系統前端

## 技術棧

- Vue.js 3
- Vuex 4
- Vue Router 4
- Element Plus
- Axios
- QRCode.js

## 目錄結構

```
frontend/
├── src/
│   ├── assets/         # 靜態資源
│   ├── components/     # Vue 組件
│   │   ├── TreeList.vue    # 樹木列表組件
│   │   ├── TreeForm.vue    # 樹木表單組件
│   │   └── QRCodeDialog.vue # QR 碼生成組件
│   ├── views/          # 頁面視圖
│   ├── router/         # 路由配置
│   ├── store/          # Vuex 狀態管理
│   └── utils/          # 工具函數
└── package.json        # 依賴配置
```

## 主要功能

### 1. 樹木資料管理
- 樹木列表展示
- 新增樹木記錄
- 修改樹木資訊
- 刪除樹木記錄
- 資料篩選和搜索

### 2. 歷史記錄展示
- 時間軸式歷史記錄展示
- 變更內容詳細顯示
- 操作時間和類型標記

### 3. QR 碼功能
- 單一樹木 QR 碼生成
- 批量 QR 碼生成
- QR 碼預覽和下載

### 4. 圖片管理
- 圖片上傳
- 圖片預覽
- 圖片刪除

### 5. 權限控制
- 管理員功能限制
- 操作權限驗證
- 錯誤提示

## 安裝與運行

1. 安裝依賴
```bash
npm install
```

2. 開發環境運行
```bash
npm run serve
```

3. 生產環境構建
```bash
npm run build
```

## API 接口

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

## 開發指南

### 代碼規範
- 使用 ESLint 進行代碼檢查
- 遵循 Vue.js 風格指南
- 組件命名使用 PascalCase
- 使用 TypeScript 進行類型檢查

### 組件開發
1. 組件應該保持單一職責
2. 使用 props 和 events 進行組件通信
3. 複雜邏輯應該放在 Vuex store 中
4. 使用 computed 屬性處理派生數據

### 狀態管理
- 使用 Vuex 管理全局狀態
- 模組化 store 結構
- 使用 actions 處理異步操作
- 使用 mutations 處理同步操作

## 部署說明

1. 構建生產版本
```bash
npm run build
```

2. 部署 dist 目錄到 Web 服務器

3. 配置 Nginx
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

## 維護與更新

### 版本控制
- 使用語義化版本號
- 遵循 Git Flow 工作流
- 提交信息使用約定式提交

### 錯誤處理
- 全局錯誤處理
- API 錯誤統一處理
- 用戶友好的錯誤提示

### 性能優化
- 路由懶加載
- 組件按需加載
- 圖片懶加載
- 資源壓縮 