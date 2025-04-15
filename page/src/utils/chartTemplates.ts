import barChartTemplate from "../../../charts/barChart.json" assert { type: "json" };
import pieChartTemplate from "../../../charts/pieChart.json" assert { type: "json" };
import lineChartTemplate from "../../../charts/lineChart.json" assert { type: "json" };
import scatterChartTemplate from "../../../charts/scatterPlot.json" assert { type: "json" };
import radarChartTemplate from "../../../charts/radarChart.json" assert { type: "json" };

export type ChannelInstance = {
  type: string;
  url: (string | number)[];
}

export type ChartChannel = {
  name: string;
  type: string;  
  instances: ChannelInstance[]
}

export type ChartTemplate = {
  id: string;
  // description: string;
  option: any;
  channels: ChartChannel[];
}

export const chartTemplates: ChartTemplate[] = [
  barChartTemplate satisfies ChartTemplate,
  pieChartTemplate satisfies ChartTemplate,
  lineChartTemplate satisfies ChartTemplate,
  scatterChartTemplate satisfies ChartTemplate,
  radarChartTemplate satisfies ChartTemplate,
]