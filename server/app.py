from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.entry_point import EntryPoint
from utils.data_init import DATA_PATH, DATA_DESCRIPTION, load_data_sample
from utils.logger import get_logger

logger = get_logger("app")

entry_point = EntryPoint()

app = Flask(__name__)
CORS(app)

downloadableFiles = []


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
        vast_system_state = data.get("vast_system_state")
        message_history = data.get("message_history")

        if not query:
            return jsonify({"code": 400, "message": "缺少查询文本", "data": None})

        # 使用预加载的数据样本进行处理
        result = entry_point.process_query(
            query=query,
            data_path=DATA_PATH,
            data_description=DATA_DESCRIPTION,
            data_sample=load_data_sample(),
            vast_system_state=vast_system_state,
            message_history=message_history,
        )
        logger.info(f"处理结果: {result}")

        # 检查错误
        if "error" in result:
            return jsonify({"code": 500, "message": result["error"], "data": None})

        # 如果是报告生成类型，返回文件下载
        if result.get("query_type") == "report" and "report_path" in result:
            path = result["report_path"]
            # convert WindowsPath to string
            path = str(path)
            
            downloadableFiles.append(path)
            # print(type(result["report_path"]))
            # print(result["report_path"])
            return jsonify(
                {
                    "code": 200,
                    "message": "报告生成成功",
                    "data": {
                        "query_type": "report",
                        # "report_path": path,
                        # "download_name": f"{result.get('province', '湖北')}_{result.get('year', '2022')}年能源消费分析报告.docx",
                        "markdown_content": result.get("markdown_content", "")
                    },
                }
            )
            # response = send_file(
            #     result["report_path"],
            #     mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            #     as_attachment=True,
            #     download_name=f"{result.get('province', '湖北')}_{result.get('year', '2022')}年能源消费分析报告.docx",
            # )
            # response.headers['Content-Transfer-Encoding'] = 'binary'
            # return response

        # 其他分析类型返回JSON数据
        return jsonify({"code": 200, "message": "分析成功", "data": result})

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify(
            {"code": 500, "message": f"处理请求时发生错误: {str(e)}", "data": None}
        )


@app.route("/api/download", methods=["GET"])
def download():
    try:
        # 获取下载文件名
        file_name = request.args.get("file_name")
        if not file_name:
            return jsonify({"code": 400, "message": "缺少文件名", "data": None})

        # 检查文件是否存在于可下载列表中
        if file_name not in downloadableFiles:
            return jsonify({"code": 404, "message": "文件未找到", "data": None})

        # 返回文件
        return send_file(
            file_name,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=file_name.split("/")[-1],
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify(
            {"code": 500, "message": f"处理请求时发生错误: {str(e)}", "data": None}
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
