<template>
  <div class="forest-background" :style="backgroundStyle">
    <div class="overlay"></div>
  </div>
</template>

<script>
import bgImage from '@/assets/images/MCW-6-600x400.jpg'

export default {
  name: 'ForestBackground',
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed'
      }
    }
  }
}
</script>

<style scoped>
.forest-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: -1;
  min-height: 100vh;
}
</style> 