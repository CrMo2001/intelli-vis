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
}
```

## response

数值查询
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

可视化查询

```
{
  code: number,
  message: string,
  data: {
    query_type: "visualization",
    chart_id: string,
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