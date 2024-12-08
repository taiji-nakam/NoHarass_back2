# 診断結果・基礎情報からおすすめエリアを生成します

from flask import jsonify

def do(data):
    try:
        # デバッグ用: 受け取ったデータを出力
        print("Received data:", data)

        # データが提供されていない場合のエラーレスポンス
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # 必須フィールドをチェック
        required_fields = [
            "assessmentId",
            "age_group",
            "country_origin",
            "nearest_station",
            "station_to_home",
            "budget_lower_limit",
            "budget_upper_limit"
        ]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            # ステータスコードを含めずに辞書を返す
            return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

        # 必須フィールドの値を取得
        assessment_id = data.get("assessmentId")
        age_group = data.get("age_group")
        country_origin = data.get("country_origin")
        nearest_station = data.get("nearest_station")
        station_to_home = data.get("station_to_home")
        budget_lower_limit = data.get("budget_lower_limit")
        budget_upper_limit = data.get("budget_upper_limit")
        area_fg_smaller = data.get("area_fg_smaller", False)  # デフォルトはFalse
        area_fg_average = data.get("area_fg_average", False)
        area_fg_larger = data.get("area_fg_larger", False)

        # デバッグ用: フィールドの内容を出力
        print(f"Assessment ID: {assessment_id}")
        print(f"Age Group: {age_group}")
        print(f"Country Origin: {country_origin}")
        print(f"Nearest Station: {nearest_station}")
        print(f"Station to Home: {station_to_home} minutes")
        print(f"Budget Range: {budget_lower_limit}-{budget_upper_limit}万円")
        print(f"Area Preferences: Smaller={area_fg_smaller}, Average={area_fg_average}, Larger={area_fg_larger}")

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
