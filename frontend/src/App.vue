<template>
  <div id="app">
    <ForestBackground />
    <SideBar />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'
import ForestBackground from '@/components/ForestBackground.vue'

export default {
  name: 'App',
  components: {
    SideBar,
    ForestBackground
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Arial, sans-serif;
  overflow-y: auto;
}

#app {
  min-height: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.main-content {
  margin-left: 60px; /* 與側邊欄寬度相等 */
  width: calc(100% - 60px);
  min-height: 100vh;
}
</style>