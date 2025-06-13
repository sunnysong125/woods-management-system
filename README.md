# 森林樹木管理系統 (Woods Management System)

![CI/CD](https://github.com/sunnysong125/woods-management-system/workflows/CI%2FCD%20Pipeline/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Vue](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django)

🌲 一個現代化的森林樹木數據管理平台，提供樹木資料的上傳、查詢、管理和分析功能。由 Orderble 提供技術支援。

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

## CI/CD 部署

本專案使用 GitHub Actions 實現自動化 CI/CD 流程：

- **自動測試**：每次推送自動執行前後端測試
- **Docker 建構**：自動建構並推送 Docker 映像到 Docker Hub
- **自動部署**：前端自動部署到 GitHub Pages

詳細設置說明請參考 [CI/CD 設置指南](CI_CD_SETUP.md)

## 部署架構

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   GitHub Repo   │────▶│ GitHub Actions  │────▶│   Docker Hub    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │  GitHub Pages   │     │ Production Server│
                        │   (Frontend)    │     │   (Backend)     │
                        └─────────────────┘     └─────────────────┘
```

## 貢獻指南

歡迎提交 Pull Request 或開啟 Issue！

## 授權

MIT License