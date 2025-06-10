# 🌳 Woods Management System - Frontend Dockerfile

# 階段1: 建構階段
FROM node:18-alpine AS build-stage

WORKDIR /app

# 複製依賴定義文件
COPY package*.json ./

# 安裝依賴
RUN npm ci --only=production

# 複製源代碼
COPY . .

# 建構應用
RUN npm run build

# 階段2: 生產階段
FROM nginx:1.25-alpine AS production-stage

# 安裝 curl 用於健康檢查
RUN apk add --no-cache curl

# 複製自定義nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 複製建構好的應用
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 創建非root用戶
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# 設置正確的權限
RUN chown -R nextjs:nodejs /usr/share/nginx/html
RUN chown -R nextjs:nodejs /var/cache/nginx
RUN chown -R nextjs:nodejs /var/log/nginx
RUN chown -R nextjs:nodejs /etc/nginx/conf.d
RUN touch /var/run/nginx.pid
RUN chown -R nextjs:nodejs /var/run/nginx.pid

# 切換到非root用戶
USER nextjs

# 暴露端口
EXPOSE 8080

# 健康檢查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# 啟動nginx
CMD ["nginx", "-g", "daemon off;"] 