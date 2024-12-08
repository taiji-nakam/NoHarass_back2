# 診断結果・基礎情報からおすすめエリアを生成します

from flask import jsonify

def do(data):
    # dataから基礎情報取得

    # 基礎情報をDBに登録
    ### mdlArea.pyで使う ###
    # # [db Sample] basic_infoテーブルへInsert
    # basic_info_to_insert = mymodels.basic_info(
    #     assessment_id = new_assessment_id,
    #     age_group = "30",
    #     country_origin = "USA",
    #     nearest_station = "Shibuya Station",
    #     budget_lower_limit = 80000,
    #     budget_upper_limit = 150000,
    #     area_fg_smaller = 0,
    #     area_fg_average = 1,
    #     area_fg_larger = 1
    # )
    # insert_cnt = crud.myinsert(basic_info_to_insert)
    # message = message + f"[insert to basic_info]row{insert_cnt}\n "

    # 診断結果を取得
#    # [db Sample] assessment_resultデータを取得、基礎情報と合わせてgptにおすすエリアを提案してもらう
#     result = crud.select_assessment_result(new_assessment_id)

    # プロンプト作成

    # GPTによる生成

    # 返答の解析

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

    # 参考ソース(GPT)
    # data = request.get_json()  # JSONデータを取得
    # print(data)
    # if data is None:
    #     return jsonify({"error": "Invalid JSON"}), 400
    # # 'message' プロパティが含まれていることを確認
    # message = data.get('message', 'No message provided')

    # # OpenAIのAPIキーを設定  
    # openai.api_key = os.getenv("OPEN_API_KEY")

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