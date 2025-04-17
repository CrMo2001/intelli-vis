from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.entry_point import EntryPoint
from utils.data_init import DATA_PATH, DATA_DESCRIPTION, load_data_sample

entry_point = EntryPoint()

app = Flask(__name__)
CORS(app)


@app.route("/api/test", methods=["POST"])
def test():
    data = request.get_json()
    print(data)
    return jsonify({"code": 200, "message": "请求成功", "data": data["key"].upper()})


@app.route("/api/query", methods=["POST"])
def query():
    try:
        # 获取用户查询
        data = request.get_json()
        print(data)
        query = data.get("query")

        if not query:
            return jsonify({"code": 400, "message": "缺少查询文本", "data": None})

        # 使用预加载的数据样本进行处理
        result = entry_point.process_query(
            query=query,
            data_path=DATA_PATH,
            data_description=DATA_DESCRIPTION,
            data_sample=load_data_sample(),
        )

        # 检查错误
        if "error" in result:
            return jsonify({"code": 500, "message": result["error"], "data": None})

        # 限制数据大小
        # if result.get("data") and len(result["data"]) > 100:
        #     result["data"] = result["data"][:100]
        #     result["truncated"] = True

        return jsonify({"code": 200, "message": "分析成功", "data": result})

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"code": 500, "message": f"处理请求时发生错误: {str(e)}", "data": None})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
