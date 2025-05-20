import barChartTemplate from "../../../charts/barChart.json" assert { type: "json" };
import pieChartTemplate from "../../../charts/pieChart.json" assert { type: "json" };
import lineChartTemplate from "../../../charts/lineChart.json" assert { type: "json" };
import scatterChartTemplate from "../../../charts/scatterPlot.json" assert { type: "json" };
import radarChartTemplate from "../../../charts/radarChart.json" assert { type: "json" };
// import geoMapTemplate from "../../../charts/geoMap.json" assert { type: "json" };
// export type ChannelInstance = {
//   type: string;
//   url: (string | number)[];
// }

export type ChartChannel = {
  name: string;
  type: string;
  // instances: ChannelInstance[]
}

export type ChartTemplate = {
  id: string;
  // description: string;
  // option: any;
  channels: ChartChannel[];
}

export const chartTemplates: Record<string, ChartTemplate> = {
  bar: barChartTemplate satisfies ChartTemplate,
  pie: pieChartTemplate satisfies ChartTemplate,
  line: lineChartTemplate satisfies ChartTemplate,
  scatter: scatterChartTemplate satisfies ChartTemplate,
  radar: radarChartTemplate satisfies ChartTemplate,
  // geo: geoMapTemplate satisfies ChartTemplate,
}