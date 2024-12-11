# おすすめエリアを取得します
# mdlArea内でもよいがコンフリクト可能性が高いので独立

from flask import Flask,jsonify
from db_control import crud, mymodels

def getResult(assessmentId):
    # おススメエリア情報取得
    results = crud.select_area_result(assessmentId)
    # print(f"[===areaResult===]{results}")
    # 結果をJSON形式で返却
    return jsonify(results)