import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// register echarts theme
import eChartsTheme from "./assets/eChartsTheme.json"
import { registerTheme } from 'echarts/core'

registerTheme('theme1', eChartsTheme)

const app = createApp(App)
app.mount('#app')

