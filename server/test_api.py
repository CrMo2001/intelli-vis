import requests
import json


def test_analyze_api(query, vast_system_state, message_history):
    """测试分析API端点"""
    url = "http://127.0.0.1:5000/api/query"
    payload = {
        "query": query,
        "vast_system_state": vast_system_state,
        "message_history": message_history,
    }
    headers = {"Content-Type": "application/json"}

    print(f"发送请求: {json.dumps(payload, ensure_ascii=False)}")
    response = requests.post(url, json=payload, headers=headers)

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(result)

        # 打印基本信息
        print(f"请求状态: {result['message']}")

        # 检查是否截断
        if result.get("data", {}).get("truncated"):
            print("注意: 返回数据已截断")

        # 打印数据长度
        if "data" in result and "data" in result["data"]:
            print(f"返回数据条数: {len(result['data']['data'])}")

        # 打印通道映射
        if "data" in result and "channel_mapping" in result["data"]:
            print(
                f"通道映射: {json.dumps(result['data']['channel_mapping'], indent=2, ensure_ascii=False)}"
            )

        # 打印部分数据
        if "data" in result and "data" in result["data"] and len(result["data"]["data"]) > 0:
            print(f"\n数据样例 (前3条):")
            for i, item in enumerate(result["data"]["data"][:3]):
                print(f"  {i+1}. {json.dumps(item, ensure_ascii=False)}")

        return result
    else:
        print(f"请求失败: {response.text}")
        return None


if __name__ == "__main__":
    # 测试查询
    # query = "生成2022年湖北省能源消费报告"
    # query = "查询湖北省2006年总的能源消费"
    query = "将能源消费占比图换成柱状图"

    vast_system_state = [
        {
            "id": "chart-4",
            "type": "radar",
            "bindings": [
                {"name": "field", "field": "field"},
                {"name": "series", "field": "series"},
                {"name": "value", "field": "value"},
            ],
            "title": "湖北森林资源对比",
        },
        {
            "id": "chart-0",
            "type": "bar",
            "bindings": [
                {"name": "category", "field": "industry"},
                {"name": "value", "field": "value"},
            ],
            "title": "湖北2006年各行业能源消费",
        },
        {
            "id": "chart-1",
            "type": "pie",
            "bindings": [
                {"name": "category", "field": "industry"},
                {"name": "value", "field": "proportion"},
            ],
            "title": "湖北2006年企业能源消费占比",
        },
        {
            "id": "chart-2",
            "type": "pie",
            "bindings": [
                {"name": "category", "field": "indexs"},
                {"name": "value", "field": "value"},
            ],
            "title": "2005年产品产量分布",
        },
        {
            "id": "chart-3",
            "type": "line",
            "bindings": [
                {"name": "category", "field": "industry"},
                {"name": "value", "field": "value"},
                {"name": "x", "field": "year"},
            ],
            "title": "五大行业能源消费变化",
        },
    ]
    message_history = [
        {"role": "user", "content": "查询湖北省2006年不同企业类型能源消费情况"},
        {"role": "system", "content": "create chart-0"},
        {"role": "user", "content": "查询湖北省2006年不同企业类型能源消费占比，只取最大的五个类型"},
        {"role": "system", "content": "create chart-1"},
        {"role": "user", "content": "2005年产品产量分布情况分析"},
        {"role": "system", "content": "create chart-2"},
        {"role": "user", "content": "查询最大的五个类型的企业的能源消费变化"},
        {"role": "system", "content": "create chart-3"},
        {
            "role": "user",
            "content": "对比2005年和2010年，湖北在活立木总蓄积量产量，森林蓄积量产量，森林面积产量和林地面积产量四个方面数据的变化，用雷达图展示区别",
        },
        {"role": "system", "content": "create chart-4"},
    ]

    # 运行测试
    result = test_analyze_api(query, vast_system_state, message_history)

    # 保存完整结果到文件(可选)
    if result:
        with open("api_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n完整结果已保存到 api_response.json")
