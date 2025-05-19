# /api/test
## request
```
{
  key: string,
}
```

## response
```
{
  code: number,
  message: string,
  data: string
}
```

# /api/query
## request
```
{
  query: string,
  vast_system_state?: {
    id: string,        // 前端可视化图的唯一标识符
    type: string,      // 可视化图的类型
    title: string,     // 可视化图的标题
    bindings: string     // 可视化图的格式
  }[],
  message_history?: {
    role: string,       // 消息角色（'user' 或 'system'）
    content: string     // 消息内容
  }[]
}
```

## response

### 数值查询
```
{
  code: number,
  message: string,
  data: {
    query_type: "value",
    data: [
      {
        [key: string]: string
      }
    ],
    response: string
  }
}
```

### 新建可视化查询

```
{
  code: number,
  message: string,
  data: {
    query_type: "visualization",
    chart_id: string,         // 可视化模板ID
    chart_title: string,
    channel_mapping: {
      [key: string]: string
    },
    data: [
      {
        [key: string]: string
      }
    ]
  }
}
```

### 替换现有可视化

```
{
  code: number,
  message: string,
  data: {
    query_type: "replace",
    chart_id: string,           // 可视化模板ID
    chart_title: string,
    existing_visualization_id: string,  // 要替换的前端可视化ID
    channel_mapping: {
      [key: string]: string
    },
    data: [
      {
        [key: string]: string
      }
    ]
  }
}
```

### 报告生成

```
{
  code: number,
  message: string,
  data: {
    query_type: "report",
    markdown_content: string
  }
}
```