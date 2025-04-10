from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json()
    print(data)
    return jsonify({
        'code': 200,
        'message': '请求成功',
        'data': data['key'].upper()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)