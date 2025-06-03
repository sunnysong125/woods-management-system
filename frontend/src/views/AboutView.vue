<template>
  <div class="about">
    <h1>關於 林木測繪系統</h1>
    <div class="content-box">
      <div class="about-content">
        <h2>系統介紹</h2>
        <p>林木測繪系統是一個基於Vue.js和Django的Web應用，用於林木資源管理和數據分析。</p>
        
        <h2>主要功能</h2>
        <ul>
          <li>用戶認證（登錄/註冊/註銷）</li>
          <li>用戶角色管理（管理員/註冊會員/訪客）</li>
          <li>林木資料上傳和管理</li>
          <li>資料查詢和統計分析</li>
          <li>響應式界面設計</li>
        </ul>
        
        <h2>技術棧</h2>
        <h3>前端</h3>
        <ul>
          <li>Vue.js 3.x</li>
          <li>Vuex 4.x (狀態管理)</li>
          <li>Vue Router 4.x (路由管理)</li>
          <li>Element Plus (UI組件庫)</li>
          <li>Axios (HTTP客戶端)</li>
        </ul>
        
        <h3>後端</h3>
        <ul>
          <li>Django (Web框架)</li>
          <li>Django REST framework (API開發)</li>
          <li>Pandas (資料處理)</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: 20px;
  padding-left: 80px;
  height: 100%;
  color: #fff;
}

.about-content {
  text-align: left;
}

h1 {
  margin-bottom: 20px;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

h2 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #ffffff;
}

h3 {
  color: #ffffff;
}

ul {
  padding-left: 20px;
}
</style> 