import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// register echarts theme
import eChartsTheme from "./assets/eChartsTheme.json"
import { registerTheme, registerMap } from 'echarts/core'
import hubeiGeojson from './assets/420000.json?raw' 

registerTheme('theme1', eChartsTheme)
registerMap('hubei', {geoJSON: hubeiGeojson, specialAreas: {}})

const app = createApp(App)
app.mount('#app')

