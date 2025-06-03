<template>
  <div class="home">
    <div class="content-container">
      <h1 class="title">
        <span class="title-gray">林木</span>
        <span class="title-white">測繪</span>
      </h1>
      <p class="subtitle">專業森林資源管理系統</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 60px;
}

.content-container {
  z-index: 2;
  text-align: center;
  padding: 0 20px;
}

.title {
  font-size: 5rem;
  letter-spacing: 8px;
  margin-bottom: 20px;
  white-space: nowrap;
}

.title-gray {
  color: #aaaaaa;
  font-weight: 300;
}

.title-white {
  color: white;
  font-weight: 500;
}

.subtitle {
  color: #dddddd;
  font-size: 1.8rem;
  letter-spacing: 4px;
  margin-top: 0;
}

@media (max-width: 768px) {
  .title {
    font-size: 3.5rem;
    letter-spacing: 5px;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
}
</style> 