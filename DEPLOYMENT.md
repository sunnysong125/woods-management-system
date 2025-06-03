# WoodsCarbonSink 部署指引

## 🚀 專案更新內容

本次更新主要包含：

### ✨ 新功能
- **專案權限控制**：添加了 `created_by` 字段來追蹤專案創建者
- **刪除權限管理**：專案創建者和超級管理者都可以刪除專案
- **權限檢查優化**：前端支援多種管理員身份驗證（`is_superuser`, `is_staff`, `is_admin`, `role === 'ADMIN'`）

### 🔧 技術改動
- 後端模型變更：`Project` 模型新增 `created_by` 外鍵
- 數據庫遷移：`0005_add_created_by_to_project.py`
- API 權限邏輯更新
- 前端權限檢查邏輯改進

## 📋 部署步驟

### 1. 備份重要文件
在部署前，請備份以下文件：
```bash
# 生產環境配置
backend/core/settings.py
# 媒體文件
backend/media/
# 靜態文件
backend/static/
# 數據庫（如果是文件型數據庫）
```

### 2. 後端部署

#### 方法一：使用 Git 部署（推薦）
```bash
# 在生產服務器上
cd /path/to/production/
git pull origin master

# 安裝依賴（如有新增）
pip install -r backend/requirements.txt

# 執行數據庫遷移
cd backend
python manage.py migrate trees

# 收集靜態文件
python manage.py collectstatic --noinput

# 重啟服務
systemctl restart your-django-service
```

#### 方法二：文件替換部署
如果使用文件替換，請只替換以下文件：
```bash
backend/trees/models.py
backend/trees/serializers.py
backend/trees/views.py
backend/trees/migrations/0005_add_created_by_to_project.py
```

然後執行：
```bash
cd backend
python manage.py migrate trees
systemctl restart your-django-service
```

### 3. 前端部署

前端有重要更新，需要重新構建：

```bash
# 在開發環境或CI/CD中
cd frontend
npm install
npm run build

# 將 dist/ 目錄內容部署到Web服務器
# 例如：nginx 的 html 目錄
```

### 4. 驗證部署

部署完成後，請驗證以下功能：

1. **登入功能**：確保用戶可以正常登入
2. **專案列表**：檢查專案列表是否正常顯示
3. **新增專案**：測試專案創建功能
4. **刪除權限**：
   - 專案創建者應該能看到自己專案的刪除按鈕
   - 超級管理者應該能看到所有專案的刪除按鈕
   - 其他用戶不應該看到刪除按鈕
5. **API權限**：使用API測試工具驗證刪除權限

## 🔒 權限說明

### 前端權限檢查
```javascript
// 檢查是否為管理員（任一種）
isAdmin = user.is_superuser || user.is_staff || user.is_admin || user.role === 'ADMIN'

// 檢查是否可以刪除專案
canDelete = isAdmin || project.created_by_id === currentUserId
```

### 後端權限檢查
- **查看專案**：所有人
- **創建專案**：已登入用戶
- **更新專案**：已登入用戶
- **刪除專案**：超級管理者 OR 專案創建者

## 🚨 注意事項

1. **數據庫遷移**：必須執行遷移，否則會出現錯誤
2. **現有專案**：現有專案的 `created_by` 為 `NULL`，只有超級管理者可以刪除
3. **CSRF 設定**：確保生產環境的 `CSRF_TRUSTED_ORIGINS` 包含正確的域名
4. **環境變數**：檢查所有環境變數是否正確設定

## 🐛 常見問題

### 403 錯誤
如果遇到 CSRF 403 錯誤，檢查 `settings.py` 中的：
```python
CSRF_TRUSTED_ORIGINS = [
    'https://srv.orderble.com.tw',
    'http://srv.orderble.com.tw',
]
```

### 前端無法看到刪除按鈕
確認：
1. 用戶已正確登入
2. 用戶權限設定正確
3. 專案的 `created_by_id` 正確返回

### 數據庫錯誤
如果遇到欄位不存在的錯誤，執行：
```bash
python manage.py migrate trees --fake-initial
python manage.py migrate trees
```

## 📞 支援

如果部署過程中遇到問題，請檢查：
1. 服務器日誌
2. Django 錯誤日誌
3. 網絡瀏覽器控制台錯誤

## 📝 更新日誌

**2025-06-03**
- 添加專案創建者追蹤功能
- 實施精細化權限控制
- 修復前端權限檢查邏輯
- 優化用戶體驗 