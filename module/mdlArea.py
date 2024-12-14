# 診断結果・基礎情報からおすすめエリアを生成します

from flask import jsonify
from db_control import crud, mymodels
from .mdlAssessment import getResult
import openai
import os
import json

def do(data):
    try:
        # デバッグ用: 受け取ったデータを出力
        print("Received data:", data)

        # データが提供されていない場合のエラーレスポンス
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # 必須フィールドをチェック ← エラーとりまコメントアウト
        # required_fields = [
        #     "assessmentId",
        #     "age_group",
        #     "country_origin",
        #     "nearest_station",
        #     "station_to_home",
        #     "budget_lower_limit",
        #     "budget_upper_limit"
        # ]
        # missing_fields = [field for field in required_fields if field not in data]
        # if missing_fields:
        #     # ステータスコードを含めずに辞書を返す
        #     return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

        # 診断ID取得
        targetId = data['assessmentId']
        # 基本情報データのInput
        basic_info_to_insert = mymodels.basic_info(
            assessment_id = targetId,  # assessment_idに対応
            age_group = data['formData']['age_group'],  # 年齢層
            country_origin = data['formData']['country_origin'],  # 出身国
            nearest_station = data['formData']['nearest_station'],  # 最寄り駅
            time_tostation = data['formData']['station_to_home'],
            budget_lower_limit = int(data['formData']['budget_lower_limit']),  # 予算下限（数値化）
            budget_upper_limit = int(data['formData']['budget_upper_limit']),  # 予算上限（数値化）
            area_fg_smaller = int(data['formData']['area_fg_smaller']),  # 小エリアフラグ（0 or 1）
            area_fg_average = int(data['formData']['area_fg_average']),  # 平均エリアフラグ（0 or 1）
            area_fg_larger = int(data['formData']['area_fg_larger'])  # 大エリアフラグ（0 or 1）
        )
        insert_cnt = crud.myinsert(basic_info_to_insert)
        if insert_cnt == 0:
            print("Error occurred:basic_info Insert")
            return {"error": f"An unexpected error occurred: basic_info Insert"}
        
                # 基本情報からプロンプトパラメータを生成
        pInfo = f"居住区を探している人の基本情報です。\n\
年齢層:{data['formData']['age_group']}\n\
出身国：{data['formData']['country_origin']}\n\
最寄り駅：{data['formData']['nearest_station']}\n\
最寄り駅からの所要時間:{data['formData']['station_to_home']}\n"

        # 診断結果情報の取得
        assessment_result = getResult(targetId)
        assessment_result = json.loads(assessment_result)
        pResult = f"居住区を探している人が重視しているカテゴリーの優先順位です。カテゴリーと優先度を数値化しています。"
        for item in assessment_result:
             print("item type:", type(item), "item:", item)
             category = item["category"]
             priority = str(item["priority"])
             pResult += f"- {category}: {priority}\n"


        

        print("pInfo:",pInfo)
        print("pResult:",pResult)
        

        # GPTプロンプト作成と送信
        # OpenAIのAPIキーを設定  
        openai.api_key = os.getenv("OPEN_API_KEY")
        message="おススメの東京都内の居住地は？"
        prompt = f"これから住む場所を探しています。おすすめの地域、地域の代表的な場所の緯度と経度、400字程度のおすすめ文章を出力してください{pInfo}\n{pResult}\n\
            最寄り駅が存在しない場合は、福岡周辺をターゲットにしてください。最寄り駅が存在しなった旨をおススメ文に加えてください。"
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt },
            ],
        )
        output_content = response.choices[0].message.content.strip()
        print("fromGPT:",output_content)    



        # 処理例: 推奨エリアの生成 (仮の結果を構築)
        recommended_area = "東京都渋谷区XXX丁目"
        result = {
            "area": recommended_area,
            "message": "Recommendation generated successfully",
        }

        # 辞書だけを返す（ステータスコードは含めない）
        return result

    except Exception as e:
        # サーバーエラーが発生した場合のレスポンス
        print("Error occurred:", e)
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Assessment IDを取得
    # new_assessment_id=data["assessmentId"]
    
# 必要なデータを取得
    basic_info_to_insert = mymodels.basic_info(
        assessment_id = new_assessment_id,
        # age_group = data.get("age_group")
        # country_origin = data.get("country_origin", "")
        # nearest_station = data.get("nearest_station", "")
        # budget_lower_limit = data.get("budget_lower_limit", )
        # budget_upper_limit = data.get("budget_upper_limit", )
        # area_fg_smaller = data.get("area_fg_smaller", 0)
        # area_fg_average = data.get("area_fg_average", 1)
        # area_fg_larger = data.get("area_fg_larger", 1)
    )

    insert_cnt = crud.myinsert(basic_info_to_insert)
    message = message + f"[insert to basic_info]row{insert_cnt}\n "
    
    # 参考ソース(GPT)
    # GPTプロンプト作成と送信
    # data = request.get_json()  # JSONデータを取得
    # print(data)
    # if data is None:
    # return jsonify({"error": "Invalid JSON"}), 400
    #  'message' プロパティが含まれていることを確認
    # message = data.get('message', 'No message provided')

    # prompt = f"次の質問に対して400文字以内に要約して回答してください。{message}"

    # response =  openai.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "user", "content": prompt },
    #     ],
    # )
    # # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    # output_content = response.choices[0].message.content.strip()
    # return jsonify({"message": f"{output_content}"})
    # GPTによる生成

    # 返答の解析

    # 診断結果を取得
#    # [db Sample] assessment_resultデータを取得、基礎情報と合わせてgptにおすすエリアを提案してもらう
#     result = crud.select_assessment_result(new_assessment_id)

    # おすすめエリアをDBに登録
    ### mdlArea.pyで使う ###
    # [db Sample] area_resultテーブルへInsert
    # area_result_to_insert = mymodels.area_result(
    #     assessment_id = new_assessment_id,
    #     recommended = "東京 渋谷区",
    #     note = "おススメエリア：渋谷区の説明文です"
    # )
    # insert_cnt = crud.myinsert(area_result_to_insert)
    # message = message + f"[insert to area_result]row{insert_cnt}\n "


    # 結果を構成
    print("4 OK")

    return jsonify({'area': '東京都渋谷区XXX丁目'})


    # グーグルマップと連携
