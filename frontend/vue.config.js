module.exports = {
  publicPath: '/woodsfrond/',
  
  // 添加靜態資源配置
  chainWebpack: config => {
    // 複製靜態資源到輸出目錄
    config.plugin('copy')
      .tap(args => {
        args[0].patterns.push(
          {
            from: 'public/tree_sample.csv',
            to: 'tree_sample.csv'
          },
          {
            from: 'public/favicon.png',
            to: 'favicon.png'
          },
          {
            from: 'public/favicon.ico',
            to: 'favicon.ico'
          }
        );
        return args;
      });
  },
  
  devServer: {
    proxy: {
      '/api': {
        target: 'https://srv.orderble.com.tw/woodsbackend',
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  }
} 