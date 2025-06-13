# CI/CD 設置指南 - Woods Management System

## 🚀 快速開始

本指南將幫助您在 GitHub 上設置完整的 CI/CD 流程。

## 📋 前置要求

### 1. GitHub Repository Secrets 設置

請在您的 GitHub 倉庫中設置以下 Secrets：

1. 進入 GitHub 倉庫：https://github.com/sunnysong125/woods-management-system
2. 點擊 `Settings` → `Secrets and variables` → `Actions`
3. 點擊 `New repository secret` 添加以下 secrets：

#### 必需的 Secrets：
- **DOCKERHUB_USERNAME**: 您的 Docker Hub 用戶名
- **DOCKERHUB_TOKEN**: Docker Hub Access Token（不是密碼）
  - 在 [Docker Hub](https://hub.docker.com/settings/security) 創建 Access Token

### 2. 啟用 GitHub Pages

1. 進入 `Settings` → `Pages`
2. Source 選擇 `GitHub Actions`
3. 保存設置

## 🔧 CI/CD 流程說明

### 工作流程觸發條件：
- **Push 到 main 分支**：執行完整的測試、建構、部署流程
- **Push 到 develop 分支**：執行測試和 Docker 建構
- **Pull Request 到 main**：執行測試流程
- **手動觸發**：通過 GitHub Actions 界面手動執行

### 主要步驟：

1. **前端測試** (`frontend-test`)
   - 安裝依賴
   - ESLint 代碼檢查
   - 建構前端項目
   - 上傳建構產物

2. **後端測試** (`backend-test`)
   - 設置 PostgreSQL 測試資料庫
   - 安裝 Python 依賴
   - Flake8 代碼檢查
   - 執行 Django 測試

3. **Docker 建構** (`docker-build`)
   - 建構前端 Docker 映像
   - 建構後端 Docker 映像
   - 推送到 Docker Hub

4. **部署前端** (`deploy-frontend`)
   - 部署到 GitHub Pages
   - 可選：設置自定義域名

## 📦 Docker Hub 設置

### 創建 Docker Hub Access Token：

1. 登入 [Docker Hub](https://hub.docker.com/)
2. 進入 Account Settings → Security
3. 點擊 "New Access Token"
4. 給 Token 命名（例如：`github-actions`）
5. 複製 Token 並添加到 GitHub Secrets

### Docker 映像命名：
- 前端：`<your-username>/woods-frontend`
- 後端：`<your-username>/woods-backend`

## 🌐 自定義域名設置（可選）

如果您有自定義域名（例如：woods.orderble.com.tw）：

1. 在 DNS 提供商設置 CNAME 記錄：
   ```
   CNAME woods.orderble.com.tw → sunnysong125.github.io
   ```

2. 在 `.github/workflows/ci-cd.yml` 中更新 cname 設置

3. 在 GitHub Pages 設置中添加自定義域名

## 🚦 監控 CI/CD 狀態

### 查看工作流程執行：
1. 進入 GitHub 倉庫
2. 點擊 `Actions` 標籤
3. 查看各個工作流程的執行狀態

### 添加狀態徽章到 README：
```markdown
![CI/CD](https://github.com/sunnysong125/woods-management-system/workflows/CI%2FCD%20Pipeline/badge.svg)
```

## 🛠️ 本地測試 CI/CD

### 測試前端建構：
```bash
cd frontend
npm ci
npm run lint
npm run build
```

### 測試後端：
```bash
cd backend
pip install -r requirements.txt
python manage.py test
```

### 測試 Docker 建構：
```bash
# 前端
cd frontend
docker build -t woods-frontend .

# 後端
cd backend
docker build -t woods-backend .
```

## 📝 常見問題

### Q: GitHub Actions 失敗了怎麼辦？
A: 點擊失敗的工作流程，查看詳細日誌。常見問題：
- Secrets 未正確設置
- 依賴安裝失敗
- 測試未通過

### Q: Docker Hub 推送失敗？
A: 檢查：
- DOCKERHUB_USERNAME 和 DOCKERHUB_TOKEN 是否正確
- Docker Hub 是否有足夠的存儲空間
- 網絡連接是否正常

### Q: GitHub Pages 部署失敗？
A: 確認：
- GitHub Pages 已啟用
- 建構產物路徑正確
- 沒有文件大小限制問題

## 🎯 下一步

1. **推送代碼觸發 CI/CD**：
   ```bash
   git add .
   git commit -m "feat: Setup CI/CD pipeline"
   git push origin main
   ```

2. **查看執行結果**：
   - 訪問 https://github.com/sunnysong125/woods-management-system/actions

3. **訪問部署的應用**：
   - GitHub Pages: https://sunnysong125.github.io/woods-management-system/
   - 或自定義域名（如已設置）

## 📞 需要幫助？

如有問題，請：
1. 查看 GitHub Actions 日誌
2. 檢查本文檔的常見問題
3. 在 GitHub Issues 中提問

---

🌲 Happy Deploying! 🚀 