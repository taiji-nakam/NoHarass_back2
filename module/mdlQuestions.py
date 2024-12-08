# 質問項目から診断を実施します

from flask import jsonify
from db_control import crud, mymodels

def getAll():
    # DBからすべての質問項目ID/内容を取得
    # model = mymodels.Questions
    # result = crud.myselectAll(mymodels.Customers)
    # return result

    return jsonify({'message': '[dummy]All Questions'})



