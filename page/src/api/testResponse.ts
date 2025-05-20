import { reportResponse } from "./reportResponse";

const testResponses = [
  reportResponse,
  {
    "code": 200,
    "data": {
      query_type: "report",
      doc: "# test\n\n报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容\n\n报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容\n\n报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容报告内容"
    },
    "message": "分析成功"
  },
  // {
  //   "code": 200,
  //   "data": {
  //     channelMapping: {},
  //     chart_id: "geo",
  //     data: [],
  //     query_type: "visualization"
  //   },
  //   "message": "分析成功"
  // },
  {
    "code": 200,
    "data": {
      "channel_mapping": {
        "category": "industry",
        "value": "percentage"
      },
      "chart_id": "pie",
      "chart_title": "湖北2006年企业能源消费占比",
      "data": [
        {
          "industry": "专用设备制造业",
          "percentage": 0.17,
          "value": 13.92
        },
        {
          "industry": "仪器仪表制造业",
          "percentage": 0.05,
          "value": 3.96
        },
        {
          "industry": "其他制造业",
          "percentage": 0.08,
          "value": 6.95
        },
        {
          "industry": "其他采矿业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "农副食品加工业",
          "percentage": 0.69,
          "value": 57.97
        },
        {
          "industry": "化学原料和化学制品制造业",
          "percentage": 18.74,
          "value": 1566.15
        },
        {
          "industry": "化学纤维制造业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "医药制造业",
          "percentage": 1.21,
          "value": 101.18
        },
        {
          "industry": "印刷和记录媒介复制业",
          "percentage": 0.16,
          "value": 13.43
        },
        {
          "industry": "家具制造业",
          "percentage": 0.01,
          "value": 1.08
        },
        {
          "industry": "废弃资源综合利用业",
          "percentage": 0.01,
          "value": 0.65
        },
        {
          "industry": "开采辅助活动",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "有色金属冶炼和压延加工业",
          "percentage": 1.82,
          "value": 151.88
        },
        {
          "industry": "有色金属矿采选业",
          "percentage": 0.03,
          "value": 2.17
        },
        {
          "industry": "木材加工和木、竹、藤、棕、草制品业",
          "percentage": 0.2,
          "value": 16.33
        },
        {
          "industry": "橡胶和塑料制品业",
          "percentage": 0.32,
          "value": 27.04
        },
        {
          "industry": "水的生产和供应业",
          "percentage": 0.08,
          "value": 6.89
        },
        {
          "industry": "汽车制造业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "烟草制品业",
          "percentage": 0.1,
          "value": 8.72
        },
        {
          "industry": "煤炭开采和洗选业",
          "percentage": 0.04,
          "value": 3.3
        },
        {
          "industry": "燃气生产和供应业",
          "percentage": 0.52,
          "value": 43.87
        },
        {
          "industry": "电力、热力生产和供应业",
          "percentage": 51.34,
          "value": 4292.12
        },
        {
          "industry": "电气机械及器材制造业",
          "percentage": 0.26,
          "value": 21.78
        },
        {
          "industry": "皮革、毛皮、羽毛(绒)及其制品业",
          "percentage": 0.02,
          "value": 1.39
        },
        {
          "industry": "皮革、毛皮、羽毛及其制品和制鞋业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "石油、煤炭及其他燃料加工业",
          "percentage": 0.14,
          "value": 11.39
        },
        {
          "industry": "石油和天然气开采业",
          "percentage": 0.31,
          "value": 25.96
        },
        {
          "industry": "纺织业",
          "percentage": 1,
          "value": 83.24
        },
        {
          "industry": "纺织服装、服饰业",
          "percentage": 0.16,
          "value": 13.06
        },
        {
          "industry": "计算机、通信和其他电子设备制造业",
          "percentage": 0.09,
          "value": 7.69
        },
        {
          "industry": "通用设备制造业",
          "percentage": 0.63,
          "value": 52.95
        },
        {
          "industry": "造纸和纸制品业",
          "percentage": 1.62,
          "value": 135.76
        },
        {
          "industry": "酒、饮料和精制茶制造业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "金属制品、机械和设备修理业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "金属制品业",
          "percentage": 0.16,
          "value": 12.97
        },
        {
          "industry": "铁路、船舶、航空航天和其他运输设备制造业",
          "percentage": 0,
          "value": 0
        },
        {
          "industry": "非金属矿物制品业",
          "percentage": 11.62,
          "value": 971.78
        },
        {
          "industry": "非金属矿采选业",
          "percentage": 1.17,
          "value": 97.57
        },
        {
          "industry": "食品制造业",
          "percentage": 1.05,
          "value": 87.63
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "percentage": 5.96,
          "value": 498.29
        },
        {
          "industry": "黑色金属矿采选业",
          "percentage": 0.24,
          "value": 20.35
        }
      ],
      "query_type": "visualization"
    },
    "message": "分析成功"
  },
  {
    "code": 200,
    "data": {
      "channel_mapping": {
        "category": "industry",
        "value": "percentage"
      },
      "chart_id": "pie",
      "chart_title": "湖北2006年企业能源消费前五",
      "data": [
        {
          "industry": "电力、热力生产和供应业",
          "percentage": 57.3795957873
        },
        {
          "industry": "化学原料和化学制品制造业",
          "percentage": 20.9372184241
        },
        {
          "industry": "非金属矿物制品业",
          "percentage": 12.991329132
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "percentage": 6.6614350915
        },
        {
          "industry": "有色金属冶炼和压延加工业",
          "percentage": 2.0304215651
        }
      ],
      "existing_visualization_id": "chart-0",
      "query_type": "replace"
    },
    "message": "分析成功"
  },

  {
    "code": 200,
    "data": {
      "channel_mapping": {
        "x": "industry",
        "value": "value",
        "group": "null",
      },
      "chart_id": "bar",
      "data": [
        {
          "industry": "专用设备制造业",
          "value": 13.92
        },
        {
          "industry": "仪器仪表制造业",
          "value": 3.96
        },
        {
          "industry": "其他制造业",
          "value": 6.95
        },
        {
          "industry": "其他采矿业",
          "value": 0
        },
        {
          "industry": "农副食品加工业",
          "value": 57.97
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1566.15
        },
        {
          "industry": "化学纤维制造业",
          "value": 0
        },
        {
          "industry": "医药制造业",
          "value": 101.18
        },
        {
          "industry": "印刷和记录媒介复制业",
          "value": 13.43
        },
        {
          "industry": "家具制造业",
          "value": 1.08
        },
        {
          "industry": "废弃资源综合利用业",
          "value": 0.65
        },
        {
          "industry": "开采辅助活动",
          "value": 0
        },
        {
          "industry": "有色金属冶炼和压延加工业",
          "value": 151.88
        },
        {
          "industry": "有色金属矿采选业",
          "value": 2.17
        },
        {
          "industry": "木材加工和木、竹、藤、棕、草制品业",
          "value": 16.33
        },
        {
          "industry": "橡胶和塑料制品业",
          "value": 27.04
        },
        {
          "industry": "水的生产和供应业",
          "value": 6.89
        },
        {
          "industry": "汽车制造业",
          "value": 0
        },
        {
          "industry": "烟草制品业",
          "value": 8.72
        },
        {
          "industry": "煤炭开采和洗选业",
          "value": 3.3
        },
        {
          "industry": "燃气生产和供应业",
          "value": 43.87
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 4292.12
        },
        {
          "industry": "电气机械及器材制造业",
          "value": 21.78
        },
        {
          "industry": "皮革、毛皮、羽毛(绒)及其制品业",
          "value": 1.39
        },
        {
          "industry": "皮革、毛皮、羽毛及其制品和制鞋业",
          "value": 0
        },
        {
          "industry": "石油、煤炭及其他燃料加工业",
          "value": 11.39
        },
        {
          "industry": "石油和天然气开采业",
          "value": 25.96
        },
        {
          "industry": "纺织业",
          "value": 83.24
        },
        {
          "industry": "纺织服装、服饰业",
          "value": 13.06
        },
        {
          "industry": "计算机、通信和其他电子设备制造业",
          "value": 7.69
        },
        {
          "industry": "通用设备制造业",
          "value": 52.95
        },
        {
          "industry": "造纸和纸制品业",
          "value": 135.76
        },
        {
          "industry": "酒、饮料和精制茶制造业",
          "value": 0
        },
        {
          "industry": "金属制品、机械和设备修理业",
          "value": 0
        },
        {
          "industry": "金属制品业",
          "value": 12.97
        },
        {
          "industry": "铁路、船舶、航空航天和其他运输设备制造业",
          "value": 0
        },
        {
          "industry": "非金属矿物制品业",
          "value": 971.78
        },
        {
          "industry": "非金属矿采选业",
          "value": 97.57
        },
        {
          "industry": "食品制造业",
          "value": 87.63
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 498.29
        },
        {
          "industry": "黑色金属矿采选业",
          "value": 20.35
        }
      ],
      "query_type": "visualization"
    },
    "message": "分析成功"
  },
  // {
  //   "code": 200,
  //   "data": {
  //     "data": [
  //       {
  //         "total_energy_consumption": 133955.1892
  //       }
  //     ],
  //     "query_type": "value"
  //   },
  //   "message": "分析成功"
  // },
  {
    "code": 200,
    "data": {
      "channel_mapping": {
        "category": "industry",
        "value": "proportion"
      },
      "chart_id": "pie",
      "data": [
        {
          "industry": "电力、热力生产和供应业",
          "proportion": 0.5134471052,
          "value": 4292.12
        },
        {
          "industry": "化学原料和化学制品制造业",
          "proportion": 0.1873515148,
          "value": 1566.15
        },
        {
          "industry": "非金属矿物制品业",
          "proportion": 0.116249692,
          "value": 971.78
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "proportion": 0.0596082025,
          "value": 498.29
        },
        {
          "industry": "有色金属冶炼和压延加工业",
          "proportion": 0.0181687246,
          "value": 151.88
        }
      ],
      "query_type": "visualization"
    },
    "message": "分析成功"
  },
  {
    "code": 200,
    "data": {
      "channel_mapping": {
        "series": "industry",
        "value": "value",
        "x": "year"
      },
      "chart_id": "line",
      "data": [
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1654.78,
          "year": 1104537600000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 1349.49,
          "year": 1104537600000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 124.48,
          "year": 1104537600000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1070.41,
          "year": 1104537600000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 443.88,
          "year": 1104537600000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1566.15,
          "year": 1136073600000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 4292.12,
          "year": 1136073600000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 135.76,
          "year": 1136073600000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 971.78,
          "year": 1136073600000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 498.29,
          "year": 1136073600000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1218.85,
          "year": 1167609600000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 142.32,
          "year": 1167609600000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 107.11,
          "year": 1167609600000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 950.9,
          "year": 1167609600000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 545.91,
          "year": 1167609600000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1231.85,
          "year": 1199145600000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 2693.15,
          "year": 1199145600000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 97.58,
          "year": 1199145600000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1121.06,
          "year": 1199145600000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 589.67,
          "year": 1199145600000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1428.71,
          "year": 1230768000000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3168.59,
          "year": 1230768000000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 103.76,
          "year": 1230768000000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1179.46,
          "year": 1230768000000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 600.67,
          "year": 1230768000000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1430.87,
          "year": 1262304000000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3297.2,
          "year": 1262304000000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 108.1,
          "year": 1262304000000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1211.12,
          "year": 1262304000000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 712.24,
          "year": 1262304000000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1583.77,
          "year": 1293840000000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 2868.38,
          "year": 1293840000000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 108.83,
          "year": 1293840000000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1291.76,
          "year": 1293840000000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 774.86,
          "year": 1293840000000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1731.43,
          "year": 1325376000000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 2908.08,
          "year": 1325376000000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 102.25,
          "year": 1325376000000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1336.05,
          "year": 1325376000000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 790.33,
          "year": 1325376000000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1814.27,
          "year": 1356998400000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3533.99,
          "year": 1356998400000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 88.84,
          "year": 1356998400000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1379.83,
          "year": 1356998400000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 782,
          "year": 1356998400000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1924.06,
          "year": 1388534400000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 4218.47,
          "year": 1388534400000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 88,
          "year": 1388534400000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1340.1,
          "year": 1388534400000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 764.93,
          "year": 1388534400000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1869.25,
          "year": 1420070400000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3602.85,
          "year": 1420070400000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 81.65,
          "year": 1420070400000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1214.41,
          "year": 1420070400000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 712.74,
          "year": 1420070400000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1725.17,
          "year": 1451606400000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 4031.64,
          "year": 1451606400000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 84.04,
          "year": 1451606400000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1135.41,
          "year": 1451606400000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 732.46,
          "year": 1451606400000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1404.32,
          "year": 1483228800000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3806.35,
          "year": 1483228800000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 92.76,
          "year": 1483228800000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1139.02,
          "year": 1483228800000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 783,
          "year": 1483228800000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1275.15,
          "year": 1514764800000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3819.42,
          "year": 1514764800000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 106.81,
          "year": 1514764800000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1113.88,
          "year": 1514764800000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 782.2,
          "year": 1514764800000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1291.54,
          "year": 1546300800000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3811.1327,
          "year": 1546300800000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 130.21,
          "year": 1546300800000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1145.79,
          "year": 1546300800000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 807.48,
          "year": 1546300800000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1410.56,
          "year": 1577836800000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 3936.31,
          "year": 1577836800000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 154.13,
          "year": 1577836800000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1024.2,
          "year": 1577836800000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 681.81,
          "year": 1577836800000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1553.3,
          "year": 1609459200000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 4837.3541,
          "year": 1609459200000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 203.58,
          "year": 1609459200000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1160.69,
          "year": 1609459200000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 643.17,
          "year": 1609459200000
        },
        {
          "industry": "化学原料和化学制品制造业",
          "value": 1684.4773,
          "year": 1640995200000
        },
        {
          "industry": "电力、热力生产和供应业",
          "value": 5792.6955,
          "year": 1640995200000
        },
        {
          "industry": "造纸和纸制品业",
          "value": 190.0518,
          "year": 1640995200000
        },
        {
          "industry": "非金属矿物制品业",
          "value": 1121.7629,
          "year": 1640995200000
        },
        {
          "industry": "黑色金属冶炼和压延加工业",
          "value": 677.9455,
          "year": 1640995200000
        }
      ],
      "query_type": "visualization"
    },
    "message": "分析成功"
  }
]

let counter = 0;

export function getTestResponse() {
  const response = testResponses[counter % testResponses.length];
  counter++;
  return response;
}
