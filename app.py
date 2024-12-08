from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import openai
from db_control import crud, mymodels
from module import mdlQuestions,mdlAssessment,mdlArea,mdlHello

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # CORS設定を更新
# CORS(app, resources={r"/api/*": {"origins": "https://tech0-gen-8-step3-testapp-node1-1.azurewebsites.net"}})  # CORS設定を更新

CORS(app)

# アセスメント実施
@app.route("/doAssessment", methods=['POST'])
def do_assessment():
    data = request.get_json()  # JSONデータを取得
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    return mdlAssessment.do(data), 200

# アセスメント結果取得
@app.route("/assessmentResult", methods=['GET'])
def get_assessment():
    # クエリパラメータから assessmentId を取得
    assessmentId = request.args.get('assessmentId', type=int)
    print('assessmentId:')
    print(assessmentId)
    if assessmentId is None:
        return {"error": "Missing or invalid assessmentId"}, 400
    return mdlAssessment.getResult(assessmentId), 200

# おすすめエリア生成
@app.route("/doResult", methods=['POST'])
def do_result():
    data = request.get_json()  # JSONデータを取得
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    return mdlArea.do(data), 200

# === テスト用(デプロイパッケージより) === 
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Flask start!'})

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message='Hello World by Flask')

@app.route('/api/multiply/<int:id>', methods=['GET'])
def multiply(id):
    print("multiply")
    # idの2倍の数を計算
    doubled_value = id * 2
    return jsonify({"doubled_value": doubled_value})

@app.route('/api/echo', methods=['POST'])
def echo():
    print("echo")
    data = request.get_json()  # JSONデータを取得
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    # 'message' プロパティが含まれていることを確認
    message = data.get('message', 'No message provided')
    return jsonify({"message": f"echo: {message}"})

### Sample/Test ###
@app.route('/requestGpt', methods=['GET'])
def requestGpt():

    print("requestGpt")
    data = request.get_json()  # JSONデータを取得
    print(data)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    # 'message' プロパティが含まれていることを確認
    message = data.get('message', 'No message provided')

    # OpenAIのAPIキーを設定  
    openai.api_key = os.getenv("OPEN_API_KEY")

    prompt = f"次の質問に対して400文字以内に要約して回答してください。{message}"

    response =  openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt },
        ],
    )
    # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    output_content = response.choices[0].message.content.strip()
    return jsonify({"message": f"{output_content}"})

@app.route('/dbTest', methods=['GET'])
def dbTest():
    return mdlHello.Hello()

if __name__ == '__main__':
    app.run(debug=True)
