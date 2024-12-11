
# モジュール呼び出しテスト

from flask import jsonify
from db_control import crud, mymodels
import json

def Hello():
    ### mdlAssessment.pyで使う ###
    # [db Sample] assessmentテーブルへInsert
    new_assessment_id = crud.insert_assessment()
    message = f"[insert to asssessment]newId:{new_assessment_id}\n "
    # [db Sample] assessment_answerテーブルへInsert ※assessmentテーブルへInsertの直後に使う
    answer_to_insert = [
        mymodels.assessment_answer(assessment_id = new_assessment_id,question_id=1,answer=5),
        mymodels.assessment_answer(assessment_id = new_assessment_id,question_id=2,answer=4),
        mymodels.assessment_answer(assessment_id = new_assessment_id,question_id=3,answer=3),
        mymodels.assessment_answer(assessment_id = new_assessment_id,question_id=4,answer=2),
        mymodels.assessment_answer(assessment_id = new_assessment_id,question_id=5,answer=1)
    ]
    insert_cnt = crud.myinsert_all(answer_to_insert)
    message = message +  f"[insert to assessment_answer]row:{insert_cnt}\n "

    ### mdlAssessment.py、いずれはcustominput.pyで使う ###
    # [db Sample] assessment_resultテーブルへInsert
    result_to_insert = [
        mymodels.assessment_result(assessment_id = new_assessment_id,category="safety",priority=5),
        mymodels.assessment_result(assessment_id = new_assessment_id,category="cost",priority=4),
        mymodels.assessment_result(assessment_id = new_assessment_id,category="accessibility",priority=3),
        mymodels.assessment_result(assessment_id = new_assessment_id,category="convenience",priority=2),
        mymodels.assessment_result(assessment_id = new_assessment_id,category="environment",priority=1)
    ]
    insert_cnt = crud.myinsert_all(result_to_insert)
    message = message + f"[insert to assessment_result]row{insert_cnt}\n "

    ### mdlArea.pyで使う ###
    # [db Sample] basic_infoテーブルへInsert
    basic_info_to_insert = mymodels.basic_info(
        assessment_id = new_assessment_id,
        age_group = "30",
        country_origin = "USA",
        nearest_station = "Shibuya Station",
        budget_lower_limit = 80000,
        budget_upper_limit = 150000,
        area_fg_smaller = 0,
        area_fg_average = 1,
        area_fg_larger = 1
    )
    insert_cnt = crud.myinsert(basic_info_to_insert)
    message = message + f"[insert to basic_info]row{insert_cnt}\n "
 
    # [db Sample] assessment_resultデータを取得、基礎情報と合わせてgptにおすすエリアを提案してもらう
    result = crud.select_assessment_result(new_assessment_id)
    message = message + f"[select_assessment_result]{json.dumps(result, sort_keys=True)}\n "

    ### mdlArea.pyで使う ###
    # [db Sample] area_resultテーブルへInsert
    area_result_to_insert = mymodels.area_result(
        assessment_id = new_assessment_id,
        recommended = "東京 渋谷区",
        note = "おススメエリア：渋谷区の説明文です"
    )
    insert_cnt = crud.myinsert(area_result_to_insert)
    message = message + f"[insert to area_result]row{insert_cnt}\n "

    ### mdlAreaResult.pyで使う ###
    result = crud.select_area_result(new_assessment_id)
    message = message + f"[select_area_result]{json.dumps(result, sort_keys=True)}\n "

    # message = 'Hello from sub module!'
    return jsonify({'message': message})
