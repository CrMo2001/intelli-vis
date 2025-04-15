<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from 'vue'

const dateTime = ref('')

function updateTime() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1)
  const day = String(now.getDate())
  const hour = String(now.getHours()).padStart(2, '0')
  const minute = String(now.getMinutes()).padStart(2, '0')
  const second = String(now.getSeconds()).padStart(2, '0')

  dateTime.value = `${year} 年 ${month} 月 ${day} 日 ${hour}:${minute}:${second}`
}

let timer: number = 0;
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})

</script>

<template>
  <div class="header-container">
    <div class="title-container">
      <img src="../assets/titleBackground.svg">
      <h1>能源大数据可视化平台</h1>
    </div>
    <div class="status-container">
      <div class="date-time"> {{ dateTime }}</div>
    </div>
  </div>
</template>
<style scoped>
.header-container {
  margin: 0;
  position: relative;
  height: 4vh;
  background-color: var(--color-mask-light);
  border-bottom: 0.5vh solid var(--color-mid);
}

img {
  height: 100%;
}

.title-container {
  position: absolute;
  width: 100%;
  height: 7vh;
  left: 50%;
  transform: translate(-50%, 0);
  display: flex;
  justify-content: center;
}

h1 {
  position: absolute;
  margin-top: 1vh;
  letter-spacing: 0.1cap;
  color: var(--color-extra-light);
  font-size: 3vh;
  font-weight: bold;
}

.status-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
}

.date-time {
  color: white;
  opacity: 0.5;
  font-size: 1.5vh;
  font-weight: bold;
  margin-right: 2vh;
  /* flex: 0; */
}
</style>