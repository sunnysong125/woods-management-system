#!/bin/bash

# 🌳 Woods Management System 部署腳本
# 使用方法: ./deploy.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}
echo "🚀 開始部署 Woods Management System (環境: $ENVIRONMENT)"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查 Docker 是否安裝
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝，請先安裝 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安裝，請先安裝 Docker Compose"
        exit 1
    fi
    
    log_info "Docker 環境檢查通過"
}

# 創建必要的目錄
create_directories() {
    log_info "創建必要的目錄..."
    mkdir -p nginx/ssl
    mkdir -p backend/logs
    mkdir -p frontend/dist
    log_info "目錄創建完成"
}

# 生成自簽名SSL證書（僅用於開發）
generate_ssl_cert() {
    if [ ! -f nginx/ssl/cert.pem ] || [ ! -f nginx/ssl/key.pem ]; then
        log_info "生成開發用 SSL 證書..."
        openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes -subj "/C=TW/ST=Taiwan/L=Taipei/O=Woods/OU=IT/CN=localhost"
        log_info "SSL 證書生成完成"
    fi
}

# 設置環境變數
setup_env() {
    log_info "設置環境變數..."
    
    if [ "$ENVIRONMENT" = "prod" ]; then
        # 生產環境變數
        export COMPOSE_FILE="docker-compose.yml"
        export COMPOSE_PROFILES="production"
        export DEBUG=0
    else
        # 開發環境變數
        export COMPOSE_FILE="docker-compose.yml"
        export DEBUG=1
    fi
    
    log_info "環境變數設置完成"
}

# 建構和啟動服務
deploy_services() {
    log_info "停止現有服務..."
    docker-compose down --remove-orphans
    
    log_info "建構 Docker 映像..."
    docker-compose build --no-cache
    
    log_info "啟動服務..."
    if [ "$ENVIRONMENT" = "prod" ]; then
        docker-compose --profile production up -d
    else
        docker-compose up -d db redis backend frontend
    fi
    
    log_info "等待服務啟動..."
    sleep 30
}

# 執行資料庫遷移
run_migrations() {
    log_info "執行資料庫遷移..."
    docker-compose exec backend python manage.py migrate
    
    log_info "收集靜態文件..."
    docker-compose exec backend python manage.py collectstatic --noinput
    
    log_info "資料庫設置完成"
}

# 健康檢查
health_check() {
    log_info "執行健康檢查..."
    
    # 檢查後端
    if curl -f http://localhost:8000/api/health/ &> /dev/null; then
        log_info "✅ 後端服務運行正常"
    else
        log_warn "⚠️  後端服務可能未正常啟動"
    fi
    
    # 檢查前端
    if curl -f http://localhost:8080/health &> /dev/null; then
        log_info "✅ 前端服務運行正常"
    else
        log_warn "⚠️  前端服務可能未正常啟動"
    fi
    
    # 檢查資料庫
    if docker-compose exec db pg_isready -U postgres &> /dev/null; then
        log_info "✅ 資料庫運行正常"
    else
        log_warn "⚠️  資料庫可能未正常啟動"
    fi
}

# 顯示部署結果
show_result() {
    echo ""
    echo "🎉 部署完成！"
    echo ""
    echo "📊 服務狀態："
    docker-compose ps
    echo ""
    echo "🌐 訪問地址："
    echo "   前端: http://localhost:8080"
    echo "   後端API: http://localhost:8000/api/"
    echo "   資料庫: localhost:5432"
    
    if [ "$ENVIRONMENT" = "prod" ]; then
        echo "   生產環境: https://localhost (需要配置域名)"
    fi
    
    echo ""
    echo "📋 常用命令："
    echo "   查看日誌: docker-compose logs -f [service_name]"
    echo "   重啟服務: docker-compose restart [service_name]"
    echo "   停止服務: docker-compose down"
    echo "   進入容器: docker-compose exec [service_name] bash"
}

# 主要部署流程
main() {
    log_info "Woods Management System 自動部署開始..."
    
    check_docker
    create_directories
    
    if [ "$ENVIRONMENT" = "dev" ]; then
        generate_ssl_cert
    fi
    
    setup_env
    deploy_services
    run_migrations
    health_check
    show_result
    
    log_info "部署流程完成！"
}

# 執行主要流程
main "$@" 