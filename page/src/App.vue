<script setup lang="ts">
import { ElContainer, ElHeader, ElMain, ElFooter, ElInput, ElButton, ElIcon } from 'element-plus';
import DialogBox from './components/MessageBox.vue';
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue'
// import { test } from './api/test'
import { onMounted } from 'vue'
import ChartComponent, { type ChartBinding } from './components/ChartComponent.vue';
import HeaderComponent from './components/HeaderComponent.vue';
import { id } from 'element-plus/es/locales.mjs';
import { queryAPI, testQueryAPI } from './api/query';

const userQuery = ref('')
const dialogBox = ref<InstanceType<typeof DialogBox> | null>(null)

onMounted(() => {
  // console.log('onMounted')
  // test({ key: 'hello world' }).then((res) => {
  //   response.value = res.data
  // }).catch((err) => {
  //   console.error(err)
  // })
})

type Chart = {
  id: string
  template: string
  data: any[]
  bindings: ChartBinding[]
}

type ChartViewport = {
  left: string
  top: string
  right: string
  bottom: string
}

let idCounter = 0

const charts = ref<Chart[]>([])
const chartViewports = ref<ChartViewport[]>([])


const chartViewports1 = [
  { left: "20%", top: "5%", right: "20%", bottom: "35%" },
]

const vp2 = {
  pw: 5,
  ph: 10,
  g: 5,
}
const chartViewports2 = [
  { left: `${50 + vp2.g / 2}%`, top: `${vp2.ph}%`, right: `${vp2.pw}%`, bottom: `${vp2.ph + 30}%` },
  { left: `${vp2.pw}%`, top: `${vp2.ph}%`, right: `${50 + vp2.g / 2}%`, bottom: `${vp2.ph + 30}%` },
]

const vp3 = {
  pw: 2,
  ph: 5,
  gw: 2,
  gh: 5,
  pc: 30,
}

const chartViewports5 = [
  { left: `${vp3.pc}%`, top: `${vp3.ph}%`, right: `${vp3.pc}%`, bottom: `${vp3.ph + 30}%` },
  { left: `${vp3.pw}%`, top: `${vp3.ph}%`, right: `${100 - vp3.pc + vp3.gw}%`, bottom: `${50 + vp3.gh / 2}%` },
  { left: `${100 - vp3.pc + vp3.gw}%`, top: `${vp3.ph}%`, right: `${vp3.pw}%`, bottom: `${50 + vp3.gh / 2}%` },
  { left: `${vp3.pw}%`, top: `${50 + vp3.gh / 2}%`, right: `${100 - vp3.pc + vp3.gw}%`, bottom: `${vp3.ph}%` },
  { left: `${100 - vp3.pc + vp3.gw}%`, top: `${50 + vp3.gh / 2}%`, right: `${vp3.pw}%`, bottom: `${vp3.ph}%` },
]

function addChart(chart: Chart) {
  if (!chart) {
    return
  }
  if (charts.value.length >= 5) {
    const replacedIndex = (charts.value.length - 1) % 4 + 1;
    charts.value.push(charts.value[replacedIndex])
    charts.value[replacedIndex] = charts.value[0]
    charts.value[0] = chart;
  } else {
    charts.value.push(chart)
    const newLength = charts.value.length;
    [charts.value[0], charts.value[newLength - 1]] = [charts.value[newLength - 1], charts.value[0]];
  }
  // if (charts.value.length == 0) {
  // } else {
  //   charts.value = [chart, ...charts.value]
  // }
  if (charts.value.length >= 3) {
    chartViewports.value = chartViewports5
  } else if (charts.value.length >= 2) {
    chartViewports.value = chartViewports2
  } else {
    chartViewports.value = chartViewports1
  }
}

const isQuerying = ref(false)

function getBinding(obj: any): ChartBinding[] {
  const bindings: ChartBinding[] = []
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key]
      bindings.push({ name: key, field: value })
    }
  }
  return bindings
}

function handleResponse(data: any) {
  if (data["query_type"] == "visualization") {
    const chartData = data["data"];
    const templateId = data["chart_id"];
    const bindings = getBinding(data["channel_mapping"]);
    const chart = {
      id: `chart-${idCounter++}`,
      template: templateId,
      data: chartData,
      bindings: bindings
    }
    addChart(chart)
    dialogBox.value?.addMessage({
      content: '查询成功，图表已生成',
      sender: 'assistant'
    })
  } else {
    const dataObj = data["data"][0];
    const keyValues = Object.entries(dataObj).map(([key, value]) => {
      return `${key}: ${value}`
    })
    const content = keyValues.join('\n')
    dialogBox.value?.addMessage({
      content: content,
      sender: 'assistant'
    })
  }
}

function query() {
  if (!dialogBox.value) {
    return
  }
  if (isQuerying.value) {
    return
  }
  if (!userQuery.value) {
    console.log('input is empty')
    return
  }
  dialogBox.value.addMessage({
    content: userQuery.value,
    sender: 'user'
  })
  dialogBox.value.setLoading(true)
  isQuerying.value = true

  queryAPI({ query: userQuery.value }).then((res: any) => {
    console.log(res)
    if (res.code == 200) {
      const data = res.data
      console.log(data);
      handleResponse(data);
    } else {
      dialogBox.value?.addMessage({
        content: '查询失败，请稍后再试',
        sender: 'assistant'
      })
    }
  }).catch((err) => {
    console.error(err)
    dialogBox.value?.addMessage({
      content: '查询失败，请稍后再试',
      sender: 'assistant'
    })
  }).finally(() => {
    isQuerying.value = false
    dialogBox.value?.setLoading(false)
  })
  userQuery.value = ''
}

</script>

<template>
  <div class="background"></div>
  <el-container class="app-container">
    <el-header class="app-header">
      <HeaderComponent />
    </el-header>
    <el-main class="app-main">
      <div class="charts-container">
        <transition-group name="list" tag="div">
          <div v-for="(chart, index) in charts.slice(0, 5)" :key="chart.id" class="chart-container" :style="{
            left: chartViewports[index].left,
            top: chartViewports[index].top,
            right: chartViewports[index].right,
            bottom: chartViewports[index].bottom
          }">
            <ChartComponent :id="chart.id" :key="chart.id" :template="chart.template" :data="chart.data"
              :bindings="chart.bindings" />
            <!-- <p>{{ chart.id }}</p> -->
          </div>
        </transition-group>
      </div>

      <div class="dialog-container">
        <div class="dialog-background">
          <img src="./assets/cornerArc.svg" style="width:2vh;">
          <img src="./assets/cornerArc.svg" style="width:2vh; rotate:90deg; position:absolute; right:0;">
        </div>
        <div class="dialog-title">AI 助手</div>
        <div class="message-container">
          <DialogBox ref="dialogBox" />
        </div>
        <div class="divider"></div>
        <div class="input-container">
          <input placeholder="请输入查询内容" v-model="userQuery" class="input-textarea" />
          <button @click=query class="query-button">
            <ElIcon>
              <Search />
            </ElIcon>
            查询
          </button>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.app-container {
  height: 100vh;
}

.app-header {
  padding: 0;
  height: auto;
}

.app-main {
  /* background-color: var(--color-dark); */
  padding: 0;
  overflow: hidden;
}

.charts-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-container {
  position: absolute;
  /* background-color: aqua; */
  /* border: 1px solid #32a1ce; */
  transition: all 0.3s ease;
}

.app-footer {
  background-color: var(--color-1);
  border-top: 0.5vh solid var(--color-2);
  position: relative;
  height: 8vh;
}

.dialog-container {
  position: absolute;
  left: 30%;
  right: 30%;
  top: 70%;
  bottom: 0%;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dialog-background {
  border-radius: 2vh 2vh 0 0;
  background-color: var(--color-mask);
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.dialog-title {
  padding: 1vh;
  color: white;
  font-weight: bold;
  font-size: 1.8vh;
}

.message-container {
  flex: 1;
  width: 100%;
  height: 10px;
  /* background-color: aqua; */
}

.divider {
  height: 3px;
  width: 90%;
  background-color: var(--color-mid);
}

.input-container {
  width: 100%;
  height: 3.5vh;
  padding: 1.2vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input-textarea {
  flex: 1;
  height: 100%;
  margin: 0 1vh 0 2vh;
  padding: 0 2vh;
  border-radius: 1vh;
  font-size: 1.5vh;
  background-color: transparent;
  color: white;
  border: 1.5px solid var(--color-light);
}

.input-textarea:focus {
  outline: none;
  border: 1.5px solid var(--color-light);
}

.query-button {
  margin-right: 2vh;
  padding: 0 1.5vh;
  height: 100%;
  border-radius: 1vh;

  background-color: transparent;
  color: var(--color-light);
  border: 1.5px solid var(--color-light);
  font-size: 1.5vh;
  font-weight: bold;

  transition: all 0.3s ease;
}

.query-button:hover {
  background-color: var(--color-light);
  color: var(--color-dark);
  border: 1.5px solid var(--color-light);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  height: 0;
  opacity: 0;
}

.background {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url('./assets/background.png');
  background-size: cover;
  opacity: 0.03;
  z-index: -1;
}
</style>
