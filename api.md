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
```
{
  code: number,
  message: string,
  data: {
    chart_id: string,
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