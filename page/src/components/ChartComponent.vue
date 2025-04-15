<script setup lang="ts">
import { chartTemplates } from '../utils/chartTemplates';
import { onMounted } from 'vue';
import * as echarts from 'echarts'

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

function setValueByUrl(object: any, url: (string | number)[], value: any) {
  const lastKey = url[url.length - 1];
  let current = object;
  for (let i = 0; i < url.length - 1; i++) {
    const key = url[i]
    if (!current[key]) {
      current[key] = {};
    }
    current = current[key];
  }
  current[lastKey] = value;
}

function resizeChart() {
  if (chart) {
    chart.resize();
  }
}

onMounted(() => {
  const chartContainer = document.getElementById(props.id);
  if (chartContainer) {
    chart = echarts.init(chartContainer, "theme1");
    const chartTemplate = chartTemplates.find(template => template.id === props.template);
    if (!chartTemplate) {
      console.error(`Chart template ${props.template} not found`);
      return;
    }
    const option = JSON.parse(JSON.stringify(chartTemplate.option));
    for (let channel of chartTemplate.channels) {
      const binding = props.bindings.find(binding => binding.name === channel.name);
      if (!binding) {
        continue;
      }
      for (let instance of channel.instances) {
        if (instance.type == "data") {
          const data = props.data.map(item => item[binding.field]);
          setValueByUrl(option, instance.url, data);
        } else if (instance.type == "name") {
          setValueByUrl(option, instance.url, binding.field);
        } else {
          console.error(`Unknown instance type: ${instance.type}`);
        }
      }
    }
    console.log(option);
    chart.setOption(option);
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
  width: 100%;
  height: 100%;
}
</style>