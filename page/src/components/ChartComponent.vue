<script setup lang="ts">
import { chartTemplates } from '../utils/chartTemplates';
import { onMounted } from 'vue';
import * as echarts from 'echarts'
import { chartBuilders } from '../utils/chartBuilder';

export type ChartBinding = {
  name: string;
  field: string;
}

const props = defineProps<{
  id: string;
  template: string;
  data: any[];
  bindings: ChartBinding[];
  title: string;
}>()

const emits = defineEmits<{
  (e: 'chart-move', event: MouseEvent): void;
}>()

function handleMouseDown(e: MouseEvent) {
  emits('chart-move', e)
}

let chart: echarts.ECharts | null = null

function resizeChart() {
  if (chart) {
    chart.resize();
  }
}

onMounted(() => {
  const chartContainer = document.getElementById(props.id);
  if (chartContainer) {
    chart = echarts.init(chartContainer, "theme1");
    const chartTemplate = chartTemplates[props.template];
    if (!chartTemplate) {
      console.error(`Chart template ${props.template} not found`);
      return;
    }
    const chartBuilder = chartBuilders[props.template];
    if (!chartBuilder) {
      console.error(`Chart builder for type ${props.template} not found`);
      return;
    }
    const chartOption = chartBuilder.build(chartBuilder.option, props.data, props.bindings);
    chart.setOption(chartOption, true);
    console.log(chartOption);

    const resizeObserver = new ResizeObserver(() => { resizeChart() })
    resizeObserver.observe(chartContainer)
    // window.addEventListener('resize', function () {
    //   resizeChart();
    // });
  }
});

defineExpose({
  resizeChart,
})

</script>

<template>
  <div class="chart-background">
    <img src="../assets/cornerArc.svg" style="width:2vh; position: absolute;">
    <img src="../assets/cornerArc.svg" style="width:2vh; position: absolute; right:0; rotate:90deg;">
    <img src="../assets/cornerArc.svg" style="width:2vh; position: absolute; right:0; bottom:0; rotate:180deg;">
    <img src="../assets/cornerArc.svg" style="width:2vh; position: absolute; bottom:0; rotate:270deg;">
  </div>
  <div class="chart-header">
    <div class="chart-title">{{ props.title }}</div>
    <div class="moving-icon" @mousedown="handleMouseDown" style="height: 1.5vh">
      <svg xmlns="http://www.w3.org/2000/svg" height="150%" viewBox="0 0 24 24" fill="none">
        <g id="Interface / Drag_Horizontal">
          <g id="Vector">
            <path
              d="M18 14C17.4477 14 17 14.4477 17 15C17 15.5523 17.4477 16 18 16C18.5523 16 19 15.5523 19 15C19 14.4477 18.5523 14 18 14Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M12 14C11.4477 14 11 14.4477 11 15C11 15.5523 11.4477 16 12 16C12.5523 16 13 15.5523 13 15C13 14.4477 12.5523 14 12 14Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M6 14C5.44772 14 5 14.4477 5 15C5 15.5523 5.44772 16 6 16C6.55228 16 7 15.5523 7 15C7 14.4477 6.55228 14 6 14Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M18 8C17.4477 8 17 8.44772 17 9C17 9.55228 17.4477 10 18 10C18.5523 10 19 9.55228 19 9C19 8.44772 18.5523 8 18 8Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M12 8C11.4477 8 11 8.44772 11 9C11 9.55228 11.4477 10 12 10C12.5523 10 13 9.55228 13 9C13 8.44772 12.5523 8 12 8Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path
              d="M6 8C5.44772 8 5 8.44772 5 9C5 9.55228 5.44772 10 6 10C6.55228 10 7 9.55228 7 9C7 8.44772 6.55228 8 6 8Z"
              class="move-icon-path" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </g>
        </g>
      </svg>
    </div>
  </div>
  <div class="chart-container" :id="props.id">

  </div>
</template>

<style scoped>
.chart-background {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: var(--color-mask);
  border-radius: 2vh;
  z-index: -1;
}

.chart-header {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  padding: 1.5vh;
}

.chart-title {
  color: white;
  font-size: 1.5vh;
  font-weight: bold;
}

.moving-icon {
  background-color: transparent;
  color: var(--color-light);
  border: none;
  border-radius: 1vh;
  padding: 0;
  margin-left: auto;
  cursor: pointer;
}

.move-icon-path {
  stroke: var(--color-light);
  transition: all 0.3s ease;
}

.chart-container {
  position: relative;
  width: 100%;
  top: 3vh;
  height: calc(100% - 3vh);
}
</style>