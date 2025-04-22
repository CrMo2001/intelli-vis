import type { ChartBinding } from "../components/ChartComponent.vue";

type ChartBuilder = {
  option: any;
  build: (option: any, data: any[], channel: ChartBinding[]) => any;
};

function getDataColumn(data: any[], field: string) {
  const column = data.map((row) => {
    const value = row[field];
    if (value === undefined || value === null) {
      return null;
    }
    return value;
  });
  return column;
}

function groupBy(data: any[], field: string) {
  const groupedData: Record<string, any[]> = {};
  for (const item of data) {
    const key = item[field];
    if (!groupedData[key]) {
      groupedData[key] = [];
    }
    groupedData[key].push(item);
  }
  return groupedData;
}

function findRequiredFields(requiredFields: string[], bindings: ChartBinding[]) {
  const result: string[] = [];
  for (const field of requiredFields) {
    const binding = bindings.find((binding) => binding.name === field);
    if (binding) {
      result.push(binding.field);
    } else {
      throw new Error(`Binding is not matched, missing: ${field}`);
    }
  }
  return result;
}

export const chartBuilders: Record<string, ChartBuilder> = {
  bar: {
    option: {
      legend: { "data": ["Direct", "Email", "Union Ads", "Video Ads", "Search"] },
      tooltip: { "trigger": "axis", "axisPointer": { "type": "shadow" } },
      grid: { "left": "3%", "right": "4%", "bottom": "3%", "containLabel": true },
      xAxis: [
        {
          type: "category",
          "data": ["Mon"],
          axisTick: { "alignWithLabel": true },
          splitLine: { "show": false }
        }
      ],
      yAxis: [{ "type": "value" }],
      series: [{ "name": "Direct", "type": "bar", "barWidth": "60%", "data": [10] }]
    },
    build: (option: any, data: any[], bindings: ChartBinding[]) => {
      const result = JSON.parse(JSON.stringify(option));

      const requiredFields = ["group", "x", "value"];
      const [group, x, value] = findRequiredFields(requiredFields, bindings);
      // category
      // result.xAxis[0].data = getDataColumn(data, category);
      // value
      // result.series[0].data = getDataColumn(data, value);
      // result.series[0].name = value;

      let firstData = data;

      if(!group || group == x) {
        if (group == x) {
          console.warn("category and x are the same")
        }
        const series = [{
          name: value,
          type: "bar",
          barWidth: "60%",
          data: getDataColumn(data, value)
        }]
        result.series = series;
        delete result.legend;
      } else {
        const groupedData = groupBy(data, group);
        const series = Object.keys(groupedData).map((key) => {
          return {
            name: key,
            type: "bar",
            // barWidth: "60%",
            data: getDataColumn(groupedData[key], value)
          };
        });
        result.series = series;
        firstData = groupedData[Object.keys(groupedData)[0]];
        // result.legend.data = Object.keys(groupedData);
        result.legend.data = groupedData.keys;
      }
      result.xAxis[0].data = getDataColumn(firstData, x)
      result.xAxis[0].name = x;

      return result;
    }
  },
  line: {
    option: {
      "tooltip": { "trigger": "axis" },
      "legend": { "data": ["Email", "Union Ads"] },
      "grid": { "left": "3%", "right": "4%", "bottom": "3%", "containLabel": true },
      "xAxis": {
        "type": "category",
        "boundaryGap": false, "data": [1104537600000]
      },
      "yAxis": { "type": "value" },
      "series": [
        { "name": "Email", "type": "line", "data": [120] },
        { "name": "Union Ads", "type": "line", "data": [220] }
      ]
    },
    build: (option: any, data: any[], bindings: ChartBinding[]) => {
      const result = JSON.parse(JSON.stringify(option));

      const requiredFields = ["series", "x", "value"];
      const [group, x, value] = findRequiredFields(requiredFields, bindings);

      let firstData = data;
      if (!group || group == x) {
        if (group == x) {
          console.warn("group and x are the same")
        }
        const series = [{
          name: value,
          type: "line",
          data: getDataColumn(data, value)
        }]
        result.series = series;
        delete result.legend;
      } else {
        const groupedData = groupBy(data, group);
        const series = Object.keys(groupedData).map((key) => {
          return {
            name: key,
            type: "line",
            data: getDataColumn(groupedData[key], value)
          };
        });
        result.series = series;
        firstData = groupedData[Object.keys(groupedData)[0]];
        console.log(result.legend, "legend")
        result.legend.data = Object.keys(groupedData);
      }

      result.xAxis.data = getDataColumn(firstData, x)
      if (result.xAxis.data.every((item: any) => typeof item === "number" && item > 1e10)) {
        result.xAxis.data = result.xAxis.data.map((item: any) => {
          const date = new Date(item);
          return date.toLocaleDateString(); // Format the date as needed
        });
      }
      result.xAxis.name = x;

      return result;
    }
  },
  scatter: {
    option: {
      "xAxis": {},
      "yAxis": {},
      "series": [
        {
          "symbolSize": 20,
          "data": [
            [10, 8.04],
            [10, 8.04]
          ],
          "type": "scatter"
        }
      ]
    },
    build(option, data, channel) {
      const result = JSON.parse(JSON.stringify(option));
      const requiredFields = ["x", "y"];
      const [x, y] = findRequiredFields(requiredFields, channel);

      // x, y
      result.series[0].data = data.map((item) => {
        return [item[x], item[y]];
      });
      result.xAxis.name = x;
      result.yAxis.name = y;

      return result;
    }
  },
  pie: {
    option: {
      "tooltip": { "trigger": "item" },
      "legend": { "top": "5%", "left": "center" },
      "series": [
        {
          "name": "Access From",
          "type": "pie",
          "radius": ["40%", "70%"],
          "avoidLabelOverlap": false,
          "itemStyle": { "borderRadius": 10, "borderColor": "#000", "borderWidth": 2 },
          "label": { "show": false, "position": "center" },
          // "emphasis": { "label": { "show": true, "fontSize": 40, "fontWeight": "bold" } },
          "labelLine": { "show": false },
          "data": [
            { "value": 1048, "name": "Search Engine" },
            { "value": 735, "name": "Direct" }
          ]
        }
      ]
    },
    build(option, data, channel) {
      const result = JSON.parse(JSON.stringify(option));
      const requiredFields = ["category", "value"];
      const [category, value] = findRequiredFields(requiredFields, channel);

      // name, value
      result.series[0].data = data.map((item) => {
        return { name: item[category], value: item[value] };
      });
      result.series[0].name = category;
      return result;
    }
  },
  radar: {
    option: {
      "legend": { "data": ["Allocated Budget", "Actual Spending"] },
      "radar": {
        "indicator": [
          { "name": "Sales", "max": 6500 },
          { "name": "Administration", "max": 16000 },
          { "name": "Information Technology", "max": 30000 },
          { "name": "Customer Support", "max": 38000 },
          { "name": "Development", "max": 52000 },
          { "name": "Marketing", "max": 25000 }
        ]
      },
      "series": [
        {
          // "name": "Budget vs spending",
          "type": "radar",
          "data": [
            { "value": [4200, 3000, 20000, 35000, 50000, 18000], "name": "Allocated Budget" },
            { "value": [5000, 14000, 28000, 26000, 42000, 21000], "name": "Actual Spending" }
          ]
        }
      ]
    },
    build(option, data, channel) {
      const result = JSON.parse(JSON.stringify(option));
      const requiredFields = ["series", "field", "value"];
      const [series, field, value] = findRequiredFields(requiredFields, channel);

      const groupedData = groupBy(data, series);
      const fields = new Set<string>();
      for (const item of data) {
        fields.add(item[field]);
      }
      const fieldsArray = Array.from(fields);
      const indicators = fieldsArray.map((field) => {
        return {
          name: field,
          // max: Math.max(...data.map((item) => item[field]))
        };
      });
      result.radar.indicator = indicators;

      const seriesData = Object.keys(groupedData).map((key) => {
        const sortedData = groupedData[key].sort((a, b) => {
          return fieldsArray.indexOf(a[field]) - fieldsArray.indexOf(b[field]);
        })
        return {
          name: key,
          value: getDataColumn(sortedData, value)
        };
      });
      result.series[0].data = seriesData;

      result.legend.data = groupedData.keys;

      return result;
    },
  },
  geo: {
    option: {
      visualMap: {
        left: 'right',
        min: 0,
        max: 10,
        inRange: {
          color: [
            "rgb(16, 97, 132)",
            "rgb(136, 219, 255)",
          ]
        },
        text: ['High', 'Low'],
        calculable: true
      },
      series: [
        {
          name: 'hubei',
          type: 'map',
          // roam: true,
          map: 'hubei',
          emphasis: {
            label: {
              show: true
            }
          },

          data: [
            { name: "襄阳市", value: 1 },
            { name: "宜昌市", value: 2 },
            { name: "恩施土家族苗族自治州", value: 3 },
            { name: "仙桃市", value: 4 },
            { name: "咸宁市", value: 5 },
            { name: "荆州市", value: 6 },
            { name: "十堰市", value: 7 },
            { name: "武汉市", value: 8 },
            { name: "随州市", value: 9 },
            { name: "黄石市", value: 10 },
            { name: "黄冈市", value: 11 },
            { name: "天门市", value: 12 },
            { name: "潜江市", value: 13 },
            { name: "荆门市", value: 14 },
            { name: "孝感市", value: 15 },
            { name: "神农架林区", value: 16 },
            { name: "鄂州市", value: 17 },
          ]
        }
      ]
    },
    build(option, data, channel) {
      return option;
    },
  }
};
