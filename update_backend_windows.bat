@echo off
chcp 65001 >nul

echo 🔄 開始更新後端服務（Windows版本）...

REM 檢查是否在正確的目錄
if not exist "backend\manage.py" (
    echo ❌ 錯誤：請在專案根目錄執行此腳本
    echo 當前目錄：%CD%
    echo 請確保您在包含backend資料夾的目錄中
    pause
    exit /b 1
)

echo 📁 當前工作目錄：%CD%

REM 激活虛擬環境（如果存在）
if exist "woods-env\Scripts\activate.bat" (
    echo 📦 激活虛擬環境...
    call woods-env\Scripts\activate.bat
) else (
    echo ⚠️  未找到虛擬環境，使用系統Python
)

REM 進入後端目錄
echo 📂 進入後端目錄...
cd backend

REM 檢查Python版本
echo 🐍 檢查Python版本...
python --version

REM 安裝/更新依賴
echo 📦 更新Python依賴...
pip install -r requirements.txt

REM 檢查Django設置
echo 🔍 檢查Django設置...
python manage.py check

REM 收集靜態文件
echo 📁 收集靜態文件...
python manage.py collectstatic --noinput

REM 執行數據庫遷移
echo 🗄️ 執行數據庫遷移...
python manage.py makemigrations
python manage.py migrate

echo.
echo ✅ 後端更新完成！
echo.
echo 📋 更新內容：
echo    - 修復CSRF跨域問題
echo    - 添加CSRF token獲取端點
echo    - 改善登入錯誤處理
echo    - 添加調試中間件
echo    - 添加測試登入端點（臨時）
echo.
echo 🚀 啟動服務器：
echo    python manage.py runserver 0.0.0.0:8085
echo.
echo 🧪 測試端點：
echo    GET  /api/users/csrf-token/     - 獲取CSRF token
echo    POST /api/users/test-login/     - 測試登入（無CSRF檢查）
echo    POST /api/users/login/          - 正常登入（有CSRF檢查）
echo.
echo 🔧 如果仍有問題，請檢查：
echo    1. 確保域名 'srv.orderble.com.tw' 在 CSRF_TRUSTED_ORIGINS 中
echo    2. 檢查前端是否正確獲取CSRF token
echo    3. 查看後端日誌以獲取詳細錯誤信息
echo    4. 嘗試使用 /api/users/test-login/ 端點測試
echo.
pause 