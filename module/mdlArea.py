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
        pInfo = f"""
            居住区を探している人の基本情報です。\n
            年齢層:{data['formData']['age_group']}\n
            出身国：{data['formData']['country_origin']}\n
            最寄り駅：{data['formData']['nearest_station']}\n
            最寄り駅からの所要時間:{data['formData']['station_to_home']}\n
            """

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
        # プロンプト生成
        prompt = f"""
            これから住む場所を探しています。以下の条件に基づいて、最寄り駅に通える範囲で、おすすめの都市名、文章、おすすめの都市の緯度、おすすめの都市の経度をJSON形式で出力してください。

            - {pInfo}
            - {pResult}

            条件:
            - 実在する駅名に基づいて回答してください。
            - 駅名が存在しない場合は、その旨を回答に含めてください。
            - おすすめの都市名 (フィールド名: "city_name")
            - おすすめ文章 (フィールド名: "description", 200字程度)
            - 都市名に一致する正確な緯度と経度を返してください。
            - 緯度 (フィールド名: "latitude")
            - 経度 (フィールド名: "longitude")

            補足:
            - 必ずJSON形式で出力してください。
            - 以下の例の形式で返してください：
            "city_name": "", "description": "", "latitude": , "longitude":  

            注意:
            - 特に重視しているカテゴリーに関してどのように判断したか文章に含めてください。
            - 最寄り駅が存在しない場合は、日本に来ない方が良い理由と共に出身国に留まるように説得してください。
            """
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt},],
        )

        # レスポンスを解析
        output_content = response.choices[0].message.content.strip()
        # デバッグ用: GPTの出力を確認
        print("GPT Raw Output:", output_content)

        # JSON解析
        try:
            # バッククォートで囲まれている場合は取り除く
            if output_content.startswith("```json") and output_content.endswith("```"):
                output_content = output_content[7:-3].strip()
            
            result = json.loads(output_content)
            # 追加情報の生成
            basic_info_to_insert = mymodels.area_result(
                assessment_id = targetId,  # assessment_idに対応
                recommended = result["city_name"],
                note = result["description"],
                latitude = result["latitude"],
                longitude = result["longitude"])
 
            insert_cnt = crud.myinsert(basic_info_to_insert)
            if insert_cnt == 0:
                print("Error occurred:area_result Insert")
                return {"error": f"An unexpected error occurred: area_result Insert"}

        except json.JSONDecodeError:
            print("レスポンスの解析に失敗しました:", output_content)

        return result
    
    except Exception as e:
        # サーバーエラーが発生した場合のレスポンス
        print("Error occurred:", e)
        return {"error": f"An unexpected error occurred: {str(e)}"}
    