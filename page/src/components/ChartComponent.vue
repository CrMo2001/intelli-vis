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
}>()

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
    <div class="chart-title">图表标题</div>
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

.chart-title {
  color: white;
  padding: 1.5vh;
  font-size: 1.5vh;
  font-weight: bold;
}

.chart-container {
  position: relative;
  width: 100%;
  top: 3vh;
  height: calc(100% - 3vh);
}
</style>