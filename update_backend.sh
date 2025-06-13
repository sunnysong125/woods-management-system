#!/bin/bash

# 🚀 後端更新部署腳本
# 用於更新已部署的後端服務

echo "🔄 開始更新後端服務..."

# 檢查是否在正確的目錄
if [ ! -f "backend/manage.py" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

# 激活虛擬環境（如果存在）
if [ -d "woods-env" ]; then
    echo "📦 激活虛擬環境..."
    source woods-env/bin/activate || source woods-env/Scripts/activate
fi

# 進入後端目錄
cd backend

# 安裝/更新依賴
echo "📦 更新Python依賴..."
pip install -r requirements.txt

# 收集靜態文件
echo "📁 收集靜態文件..."
python manage.py collectstatic --noinput

# 執行數據庫遷移
echo "🗄️ 執行數據庫遷移..."
python manage.py makemigrations
python manage.py migrate

# 重啟服務（根據您的部署方式調整）
echo "🔄 重啟後端服務..."

# 如果使用 systemd 服務
# sudo systemctl restart woods-backend

# 如果使用 supervisor
# sudo supervisorctl restart woods-backend

# 如果使用 Docker
# docker-compose restart backend

# 如果使用 gunicorn 直接運行，需要手動重啟進程
echo "⚠️  請手動重啟您的後端服務進程"

echo "✅ 後端更新完成！"
echo ""
echo "📋 更新內容："
echo "   - 修復CSRF跨域問題"
echo "   - 添加CSRF token獲取端點"
echo "   - 改善登入錯誤處理"
echo "   - 添加更詳細的日誌記錄"
echo ""
echo "🔧 如果仍有問題，請檢查："
echo "   1. 確保域名 'srv.orderble.com.tw' 在 CSRF_TRUSTED_ORIGINS 中"
echo "   2. 檢查前端是否正確獲取CSRF token"
echo "   3. 查看後端日誌以獲取詳細錯誤信息" 