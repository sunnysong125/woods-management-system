# 🌳 Woods Management System 部署指南

## 📋 目錄
- [系統概述](#系統概述)
- [先決條件](#先決條件)
- [本地開發環境](#本地開發環境)
- [CI/CD 部署](#cicd-部署)
- [生產環境部署](#生產環境部署)
- [監控和維護](#監控和維護)
- [疑難排解](#疑難排解)

## 📊 系統概述

Woods Management System 是一個現代化的樹木管理系統，採用前後端分離架構：

- **前端**: Vue.js 3 + Element Plus + Vue Router
- **後端**: Django REST Framework + PostgreSQL
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **CI/CD**: GitHub Actions

## 🛠️ 先決條件

### 開發環境
- Node.js 18+
- Python 3.11+
- PostgreSQL 13+
- Docker & Docker Compose

### 生產環境
- Docker & Docker Compose
- 域名和 SSL 證書
- 至少 2GB RAM，20GB 儲存空間

## 💻 本地開發環境

### 1. 快速啟動

```bash
# 克隆專案
git clone https://github.com/your-username/woods-management.git
cd woods-management

# 使用部署腳本（推薦）
chmod +x deploy.sh
./deploy.sh dev

# 或手動啟動
docker-compose up -d db redis backend frontend
```

### 2. 前端開發

```bash
cd frontend
npm install
npm run serve
```

訪問: http://localhost:8080

### 3. 後端開發

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API 文檔: http://localhost:8000/api/

### 4. 資料庫管理

```bash
# 進入 PostgreSQL 容器
docker-compose exec db psql -U postgres -d woodsdb

# 備份資料庫
docker-compose exec db pg_dump -U postgres woodsdb > backup.sql

# 還原資料庫
docker-compose exec -T db psql -U postgres woodsdb < backup.sql
```

## 🚀 CI/CD 部署

### 1. GitHub Repository 設置

1. **建立 GitHub Repository**
2. **設定 Secrets** (Settings → Secrets and variables → Actions):
   ```
   DOCKERHUB_USERNAME: your-docker-username
   DOCKERHUB_TOKEN: your-docker-token
   ```

3. **啟用 GitHub Pages** (Settings → Pages):
   - Source: GitHub Actions

### 2. 推送代碼觸發部署

```bash
# 推送到 main 分支觸發生產部署
git add .
git commit -m "🚀 Deploy Woods Management System"
git push origin main

# 推送到 develop 分支觸發開發測試
git push origin develop
```

### 3. 部署流程

CI/CD Pipeline 包含以下階段：

1. **前端測試建構**
   - ESLint 代碼檢查
   - 建構生產版本
   - 上傳 artifacts

2. **後端測試**
   - Flake8 代碼檢查
   - 單元測試執行
   - 覆蓋率報告

3. **Docker 建構**
   - 建構前後端 Docker 映像
   - 推送到 Docker Hub

4. **部署**
   - 前端部署到 GitHub Pages
   - 後端 Docker 映像可用於生產部署

## 🏭 生產環境部署

### 1. 伺服器準備

```bash
# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安裝 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 克隆專案
git clone https://github.com/your-username/woods-management.git
cd woods-management
```

### 2. SSL 證書設置

```bash
# 使用 Let's Encrypt（推薦）
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# 複製證書到 nginx 目錄
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

### 3. 環境變數設置

創建 `.env` 檔案：

```bash
# .env
DEBUG=0
SECRET_KEY=your-super-secret-key
DATABASE_URL=postgres://postgres:your-db-password@db:5432/woodsdb
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Email 設置（可選）
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. 生產部署

```bash
# 生產環境部署
./deploy.sh prod

# 或手動部署
docker-compose --profile production up -d
```

### 5. 域名和防火牆設置

```bash
# 開放端口
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22

# DNS 設置
# A 記錄: your-domain.com → your-server-ip
# CNAME: www.your-domain.com → your-domain.com
```

## 📈 監控和維護

### 1. 日誌監控

```bash
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# 日誌檔案位置
tail -f backend/logs/django.log
tail -f /var/log/nginx/access.log
```

### 2. 健康檢查

```bash
# 服務狀態檢查
docker-compose ps

# 健康檢查端點
curl http://localhost/health
curl http://localhost:8000/api/health/

# 資料庫連接檢查
docker-compose exec backend python manage.py check --database default
```

### 3. 備份策略

```bash
# 資料庫備份腳本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U postgres woodsdb > "backup_${DATE}.sql"

# 設置定時備份
crontab -e
# 每日 2AM 備份
0 2 * * * /path/to/backup-script.sh
```

### 4. 更新部署

```bash
# 拉取最新代碼
git pull origin main

# 重建和重啟服務
docker-compose build --no-cache
docker-compose up -d

# 執行資料庫遷移
docker-compose exec backend python manage.py migrate
```

## 🔧 疑難排解

### 常見問題

#### 1. 前端無法連接後端 API

**症狀**: CORS 錯誤、API 請求失敗
**解決方案**:
```bash
# 檢查後端服務狀態
docker-compose ps backend

# 檢查 CORS 設置
docker-compose exec backend python manage.py shell
>>> from django.conf import settings
>>> print(settings.CORS_ALLOWED_ORIGINS)
```

#### 2. 資料庫連接失敗

**症狀**: Django 無法連接 PostgreSQL
**解決方案**:
```bash
# 檢查資料庫服務
docker-compose ps db

# 測試資料庫連接
docker-compose exec db psql -U postgres -d woodsdb -c "SELECT 1;"

# 重啟資料庫服務
docker-compose restart db
```

#### 3. SSL 證書問題

**症狀**: HTTPS 連接失敗
**解決方案**:
```bash
# 檢查證書檔案
ls -la nginx/ssl/

# 驗證證書
openssl x509 -in nginx/ssl/cert.pem -text -noout

# 重新生成自簽名證書（開發用）
./deploy.sh dev
```

#### 4. Docker 容器記憶體不足

**症狀**: 容器頻繁重啟、OOM 錯誤
**解決方案**:
```bash
# 檢查系統資源
docker stats

# 清理未使用的映像和容器
docker system prune -a

# 調整 Docker Compose 記憶體限制
# 在 docker-compose.yml 中添加：
# deploy:
#   resources:
#     limits:
#       memory: 1G
```

### 效能優化

#### 1. 資料庫優化

```sql
-- 檢查慢查詢
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- 建立索引
CREATE INDEX CONCURRENTLY idx_trees_project_id ON trees(project_id);
```

#### 2. 前端優化

```bash
# 啟用 Gzip 壓縮 (已在 nginx.conf 中配置)
# 使用 CDN 分發靜態資源
# 實施代碼分割和懶加載
```

#### 3. 快取策略

```bash
# Redis 快取配置
docker-compose exec redis redis-cli info memory

# Django 快取設置
# settings.py 中配置 Redis 快取
```

## 📞 支援和聯絡

如有部署問題，請：
1. 檢查本文檔的疑難排解章節
2. 查看 GitHub Issues
3. 提交新的 Issue 並附上日誌

---

**最後更新**: 2024年1月
**版本**: 1.0.0
**維護團隊**: Woods Development Team 