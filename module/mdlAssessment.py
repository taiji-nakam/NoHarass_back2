# 質問項目から診断を実施します

from flask import jsonify
from db_control import crud, mymodels
from flask import Flask, request

def do(data):
    # dataから質問回答を取得
    print(data)
    
    # 診断をDBに登録
    new_assessment_id = crud.insert_assessment()

    # 診断回答をDBに登録
    #TODO:questionValues(questionId：value)が渡されたら登録実装
    
    # 診断結果をDBに登録
    result_to_insert = [
        mymodels.assessment_result(
            assessment_id=new_assessment_id,
            category=category,
            priority=priority
        )
        for category, priority in data['categoryAverages'].items()
    ]
    # 登録処理
    insert_cnt = crud.myinsert_all(result_to_insert)

    return jsonify({'assessment_id': new_assessment_id})

def getResult(assessmentId):
    # dataから質問回答を取得
    print('ID:')
    print(assessmentId)
    # 診断結果取得
    return crud.select_assessment_result(assessmentId)
    # 結果をJSON形式で返却
    return jsonify(results)

app = Flask(__name__)

@app.route('/doAssessment', methods=['POST'])
def do_assessment():
    data = request.json
    return do(data)

@app.route('/assessmentResult', methods=['GET'])
def assessment_result():
    assessment_id = request.args.get('assessmentId')
    return getResult(assessment_id)