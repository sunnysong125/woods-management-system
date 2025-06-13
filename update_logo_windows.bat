@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 更新 Orderble Logo 和 Favicon - Windows
echo ========================================
echo.

:: 設置顏色
for /f "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

:: 彩色輸出函數
:colorEcho
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof

echo [信息] 檢查前端目錄...
if not exist "frontend" (
    call :colorEcho 0c "錯誤: frontend 目錄不存在"
    echo.
    pause
    exit /b 1
)

echo [信息] 進入前端目錄...
cd frontend

echo [信息] 重新建構前端項目...
call npm run build
if !errorlevel! neq 0 (
    call :colorEcho 0c "錯誤: 前端建構失敗"
    echo.
    pause
    exit /b 1
)

echo.
call :colorEcho 0a "✅ Logo 和 Favicon 更新完成！"
echo.
echo.

echo [信息] 更新內容摘要:
echo - 左上角 "森" 圖標已更換為 Orderble Logo
echo - Favicon 已更新為 Orderble 圖標
echo - 頁面標題已更新為 "森林樹木管理系統 - Orderble"
echo - 支援多種favicon格式 (.png, .ico, Apple Touch Icon)
echo.

echo [信息] 檔案位置:
echo - Logo 圖片: frontend/src/assets/images/orderble-logo.png
echo - Favicon: frontend/public/favicon.png, frontend/public/favicon.ico
echo - 建構輸出: frontend/dist/
echo.

echo [下一步] 如果您正在 IIS 服務器上運行，請:
echo 1. 複製 frontend/dist/ 目錄的內容到 IIS 站點
echo 2. 確保 favicon.png 和 favicon.ico 在正確位置
echo 3. 重新載入網頁查看新的 Logo 和 Favicon
echo.

call :colorEcho 0b "更新完成！請檢查瀏覽器中的變更。"
echo.
echo.

pause 