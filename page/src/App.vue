<script setup lang="ts">
import { ElContainer, ElHeader, ElMain, ElFooter, ElInput, ElButton, ElIcon } from "element-plus";
import DialogBox from "./components/MessageBox.vue";
import { Search } from "@element-plus/icons-vue";
import { ref } from "vue";
// import { test } from './api/test'
import { onMounted } from "vue";
import ChartComponent, { type ChartBinding } from "./components/ChartComponent.vue";
import HeaderComponent from "./components/HeaderComponent.vue";
import { queryAPI, testQueryAPI } from "./api/query";
import { LayoutController } from "./utils/layoutController";

const userQuery = ref("");
const dialogBox = ref<InstanceType<typeof DialogBox> | null>(null);

onMounted(() => { });

type Chart = {
  id: string;
  title: string;
  template: string;
  data: any[];
  bindings: ChartBinding[];
};

let idCounter = 0;

const charts = ref<Chart[]>([]);
const layoutController = ref(new LayoutController());

function addChart(chart: Chart) {
  if (!chart) {
    return;
  }
  if (charts.value.length >= 5) {
    const replacedIndex = ((charts.value.length - 1) % 4) + 1;
    charts.value.push(charts.value[replacedIndex]);
    charts.value[replacedIndex] = charts.value[0];
    charts.value[0] = chart;
  } else {
    charts.value.push(chart);
    const newLength = charts.value.length;
    [charts.value[0], charts.value[newLength - 1]] = [charts.value[newLength - 1], charts.value[0]];
  }
  layoutController.value.updateVisCoords(charts.value.length);
}

const isQuerying = ref(false);

function getBinding(obj: any): ChartBinding[] {
  const bindings: ChartBinding[] = [];
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key];
      bindings.push({ name: key, field: value });
    }
  }
  return bindings;
}

function handleResponse(data: any) {
  if (data["query_type"] == "visualization") {
    const chartData = data["data"];
    const templateId = data["chart_id"];
    const bindings = getBinding(data["channel_mapping"]);
    const chart = {
      id: `chart-${idCounter}`,
      template: templateId,
      data: chartData,
      bindings: bindings,
      title: data["chart_title"] || `图表 ${idCounter + 1}`
    };
    idCounter++;
    addChart(chart);
    dialogBox.value?.addMessage({
      content: "查询成功，图表已生成",
      sender: "assistant"
    });
  } else {
    const dataObj = data["data"][0];
    const keyValues = Object.entries(dataObj).map(([key, value]) => {
      return `${key}: ${value}`;
    });
    const content = keyValues.join("\n");
    dialogBox.value?.addMessage({
      content: content,
      sender: "assistant"
    });
  }
}

function query() {
  if (!dialogBox.value) {
    return;
  }
  if (isQuerying.value) {
    return;
  }
  // if (!userQuery.value) {
  //   console.log('input is empty')
  //   return
  // }
  dialogBox.value.addMessage({
    content: userQuery.value,
    sender: "user"
  });
  dialogBox.value.setLoading(true);
  isQuerying.value = true;

  queryAPI({ query: userQuery.value })
    .then((res: any) => {
      console.log(res);
      if (res.code == 200) {
        const data = res.data;
        console.log(data);
        handleResponse(data);
      } else {
        dialogBox.value?.addMessage({
          content: "查询失败，请稍后再试",
          sender: "assistant"
        });
      }
    })
    .catch((err) => {
      console.error(err);
      dialogBox.value?.addMessage({
        content: "查询失败，请稍后再试",
        sender: "assistant"
      });
    })
    .finally(() => {
      isQuerying.value = false;
      dialogBox.value?.setLoading(false);
    });
  userQuery.value = "";
}

// moving charts
const movingIndex = ref(-1);
const hoveringIndex = ref(-1);
const isMoving = ref(false);
const cursorPos = ref({ x: 0, y: 0 });
const cursorPosOffset = ref({ x: 0, y: 0 });
const movingChartDimensions = ref({ width: 0, height: 0 });

function handleMouseEnter(index: number) {
  hoveringIndex.value = index;
  console.log("hoveringIndex", hoveringIndex.value);
}

function handleMouseLeave() {
  hoveringIndex.value = -1;
  console.log("hoveringIndex", hoveringIndex.value);
}

function startMoving(index: number, e: MouseEvent) {
  console.log("startMoving", index);
  if (isMoving.value) {
    return;
  }
  const chartContainer = document.getElementById(`container${index}`);
  if (!chartContainer) {
    console.error(`Chart container ${index} not found`);
    return;
  }
  const chartsContainer = document.getElementById("charts-container");
  if (!chartsContainer) {
    console.error(`Charts container not found`);
    return;
  }
  isMoving.value = true;
  movingIndex.value = index;
  const chartRect = chartContainer.getBoundingClientRect();
  const chartsContainerRect = chartsContainer.getBoundingClientRect();
  console.log("chartRect", chartRect);
  movingChartDimensions.value.width = chartRect.width;
  movingChartDimensions.value.height = chartRect.height;
  cursorPosOffset.value.x = e.clientX - chartRect.left + chartsContainerRect.left;
  cursorPosOffset.value.y = e.clientY - chartRect.top + chartsContainerRect.top;
  cursorPos.value.x = e.clientX;
  cursorPos.value.y = e.clientY;

  window.onmouseup = (e: MouseEvent) => {
    console.log("mouseup", e.clientX, e.clientY);
    stopMoving();
  };
  window.onmousemove = (e: MouseEvent) => {
    // console.log("mousemove", e.clientX, e.clientY);
    if (!isMoving.value) {
      return;
    }
    cursorPos.value.x = e.clientX;
    cursorPos.value.y = e.clientY;
  };
  document.body.style.cursor = "grabbing";
  // emit children event
  e.stopPropagation();
  e.preventDefault();
}

function stopMoving() {
  if (!isMoving.value) {
    return;
  }
  isMoving.value = false;

  if (hoveringIndex.value != -1) {
    const temp = charts.value[movingIndex.value];
    charts.value[movingIndex.value] = charts.value[hoveringIndex.value];
    charts.value[hoveringIndex.value] = temp;
    hoveringIndex.value = -1;
  }

  document.body.style.cursor = "default";
  onmousemove = null;
  onmouseup = null;
}
</script>

<template>
  <div class="background"></div>
  <el-container class="app-container">
    <el-header class="app-header">
      <HeaderComponent />
    </el-header>
    <el-main class="app-main">
      <div class="charts-container" id="charts-container">
        <transition-group name="list" tag="div">
          <div v-for="(chart, index) in charts.slice(0, 5)" :key="chart.id" :id="`container${index}`"
            class="chart-container" :style="{
              inset: !isMoving
                ? `${layoutController.visCoords[index].top} ${layoutController.visCoords[index].right} ${layoutController.visCoords[index].bottom} ${layoutController.visCoords[index].left}`
                : index == movingIndex
                  ? `${cursorPos.y - cursorPosOffset.y}px auto auto ${cursorPos.x - cursorPosOffset.x}px`
                  : index == hoveringIndex
                    ? `${layoutController.visCoords[movingIndex].top} ${layoutController.visCoords[movingIndex].right} ${layoutController.visCoords[movingIndex].bottom} ${layoutController.visCoords[movingIndex].left}`
                    : `${layoutController.visCoords[index].top} ${layoutController.visCoords[index].right} ${layoutController.visCoords[index].bottom} ${layoutController.visCoords[index].left}`,

              width: isMoving && index == movingIndex ? `${movingChartDimensions.width}px` : 'auto',
              height: isMoving && index == movingIndex ? `${movingChartDimensions.height}px` : 'auto',

              transition: isMoving && index == movingIndex ? 'none' : 'all 0.3s ease'
              // left: layoutController.visCoords[index].left,
              // top: layoutController.visCoords[index].top,
              // right: layoutController.visCoords[index].right,
              // bottom: layoutController.visCoords[index].bottom
            }">
            <ChartComponent :id="chart.id" :key="chart.id" :template="chart.template" :data="chart.data"
              :bindings="chart.bindings" :title="chart.title" @chart-move="(e) => startMoving(index, e)" />
          </div>
        </transition-group>
      </div>
      <div class="moving-mask-container" v-if="isMoving">
        <div v-for="(chart, index) in charts.slice(0, 5)" :key="chart.id" class="moving-mask" :style="{
          left: layoutController.visCoords[index].left,
          top: layoutController.visCoords[index].top,
          right: layoutController.visCoords[index].right,
          bottom: layoutController.visCoords[index].bottom
        }" @mouseenter="handleMouseEnter(index)" @mouseleave="handleMouseLeave"></div>
      </div>

      <div class="dialog-container" :style="{
        left: layoutController.dialogCoords.left,
        top: layoutController.dialogCoords.top,
        right: layoutController.dialogCoords.right,
        bottom: layoutController.dialogCoords.bottom
      }">
        <div class="dialog-background">
          <img src="./assets/cornerArc.svg" style="width: 2vh" />
          <img src="./assets/cornerArc.svg" style="width: 2vh; rotate: 90deg; position: absolute; right: 0" />
        </div>
        <div class="dialog-title">AI 助手</div>
        <div class="message-container">
          <DialogBox ref="dialogBox" />
        </div>
        <div class="divider"></div>
        <div class="input-container">
          <input placeholder="请输入查询内容" v-model="userQuery" class="input-textarea" />
          <button @click="query" class="query-button">
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
  /* transition: all 0.3s ease; */
}

.moving-mask-container {
  position: relative;
  translate: 0 -100%;
  width: 100%;
  height: 100%;
}

.moving-mask {
  position: absolute;
  background-color: rgba(255, 0, 0, 0.0);
}

.app-footer {
  background-color: var(--color-1);
  border-top: 0.5vh solid var(--color-2);
  position: relative;
  height: 8vh;
}

.dialog-container {
  position: absolute;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
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
  background-image: url("./assets/background.png");
  background-size: cover;
  opacity: 0.03;
  z-index: -1;
}
</style>
