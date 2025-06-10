# PostgreSQL IPv6 連接問題修正指引

## 🚨 問題描述
```
django.db.utils.OperationalError: connection to server at "srv.orderble.com.tw" (fe80::aae7:61fd:7b57:dda6), port 3360 failed: FATAL: no pg_hba.conf entry for host "fe80::aae7:61fd:7b57:dda6%15", user "odbRD", database "Wooddb", no encryption
```

這個錯誤表示 PostgreSQL 嘗試使用 IPv6 連接，但服務器的 `pg_hba.conf` 沒有配置允許 IPv6 連接。

## 🔧 解決方案

### 方案 1：強制使用 IPv4（推薦）

#### 1.1 修改數據庫配置
已經在 `backend/core/settings.py` 中進行了修改，但您還需要檢查環境變數配置。

#### 1.2 創建/修改 .env 文件
在 `backend/` 目錄下創建或修改 `.env` 文件：

```bash
# 數據庫配置
DB_ENGINE=django.db.backends.postgresql
DB_NAME=Wooddb
DB_USER=odbRD
DB_PASSWORD=您的密碼
# 重要：使用具體的IPv4地址而不是域名
DB_HOST=您的IPv4地址
# 或者如果必須使用域名，確保解析到IPv4
# DB_HOST=srv.orderble.com.tw
DB_PORT=3360
```

#### 1.3 獲取服務器 IPv4 地址
在服務器上運行以下命令獲取 IPv4 地址：
```bash
# 方法1：使用 nslookup
nslookup srv.orderble.com.tw

# 方法2：使用 dig
dig srv.orderble.com.tw A

# 方法3：使用 ping
ping -4 srv.orderble.com.tw
```

### 方案 2：修改 PostgreSQL 配置（需要 DBA 權限）

如果您有 PostgreSQL 服務器的管理權限，可以修改 `pg_hba.conf` 文件：

#### 2.1 找到 pg_hba.conf 文件
```bash
# 在 PostgreSQL 中查詢配置文件位置
sudo -u postgres psql -c "SHOW hba_file;"
```

#### 2.2 添加 IPv6 規則
在 `pg_hba.conf` 中添加：
```
# IPv6 connections
host    all             all             ::1/128                 md5
host    Wooddb          odbRD           ::/0                    md5
```

#### 2.3 重新載入配置
```bash
sudo systemctl reload postgresql
# 或
sudo -u postgres pg_ctl reload
```

### 方案 3：系統級別禁用 IPv6（謹慎使用）

如果上述方法都不可行，可以考慮在系統級別禁用 IPv6：

```bash
# 臨時禁用
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# 永久禁用（在 /etc/sysctl.conf 中添加）
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

## 🔍 診斷命令

### 檢查網絡連接
```bash
# 測試 IPv4 連接
telnet 您的IPv4地址 3360

# 測試 IPv6 連接
telnet -6 srv.orderble.com.tw 3360

# 檢查 DNS 解析
nslookup srv.orderble.com.tw
```

### 檢查 PostgreSQL 狀態
```bash
# 檢查 PostgreSQL 服務狀態
sudo systemctl status postgresql

# 檢查端口監聽
sudo netstat -tlnp | grep 3360
sudo ss -tlnp | grep 3360
```

### 測試數據庫連接
```bash
# 使用 psql 直接連接
psql -h 您的IPv4地址 -p 3360 -U odbRD -d Wooddb

# 使用 IPv4 強制連接
psql -h $(dig +short srv.orderble.com.tw A | head -n1) -p 3360 -U odbRD -d Wooddb
```

## 📝 Django 測試連接

修改配置後，測試 Django 數據庫連接：

```python
# 在 Django shell 中測試
python manage.py shell

# 執行以下 Python 代碼
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
row = cursor.fetchone()
print(row)
```

## 🚨 注意事項

1. **備份配置**：修改任何配置文件前請先備份
2. **權限需求**：修改 PostgreSQL 配置需要管理員權限
3. **重啟服務**：修改配置後可能需要重啟相關服務
4. **安全考量**：開放 IPv6 連接時請注意安全設置

## 📞 緊急聯絡

如果問題仍然存在，請提供以下信息：
1. 服務器的 IPv4 地址
2. PostgreSQL 版本
3. `pg_hba.conf` 內容（脫敏後）
4. 網絡診斷命令的輸出結果 