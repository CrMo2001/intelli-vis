import barChartTemplate from "../../../charts/barChart.json" assert { type: "json" };

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
]