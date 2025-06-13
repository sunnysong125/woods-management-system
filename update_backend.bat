@echo off
chcp 65001 >nul

echo 🔄 開始更新後端服務...

REM 檢查是否在正確的目錄
if not exist "backend\manage.py" (
    echo ❌ 錯誤：請在專案根目錄執行此腳本
    pause
    exit /b 1
)

REM 激活虛擬環境（如果存在）
if exist "woods-env\Scripts\activate.bat" (
    echo 📦 激活虛擬環境...
    call woods-env\Scripts\activate.bat
)

REM 進入後端目錄
cd backend

REM 安裝/更新依賴
echo 📦 更新Python依賴...
pip install -r requirements.txt

REM 收集靜態文件
echo 📁 收集靜態文件...
python manage.py collectstatic --noinput

REM 執行數據庫遷移
echo 🗄️ 執行數據庫遷移...
python manage.py makemigrations
python manage.py migrate

echo ✅ 後端更新完成！
echo.
echo 📋 更新內容：
echo    - 修復CSRF跨域問題
echo    - 添加CSRF token獲取端點
echo    - 改善登入錯誤處理
echo    - 添加更詳細的日誌記錄
echo.
echo 🔧 如果仍有問題，請檢查：
echo    1. 確保域名 'srv.orderble.com.tw' 在 CSRF_TRUSTED_ORIGINS 中
echo    2. 檢查前端是否正確獲取CSRF token
echo    3. 查看後端日誌以獲取詳細錯誤信息
echo.
echo ⚠️  請手動重啟您的後端服務進程
pause 