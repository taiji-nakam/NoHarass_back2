# uname() error回避
import platform
print("platform", platform.uname())

from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from datetime import datetime

from db_control.connect import engine
from db_control.mymodels import assessment,assessment_answer,assessment_result,basic_info,Customers

# assessment_resultデータ取得
def select_assessment_result(assessment_id):
    # 初期化
    result_json = None  
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()       
    query = session.query(assessment_result).filter(assessment_result.assessment_id == assessment_id)
    try:
        #トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for res in result:
            result_dict_list.append({
                "assessment_id": assessment_id,
                "category": res.category,
                "priority": res.priority
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except Exception as e:
        print(f"[select_assessment_result]例外が発生しました: {e}")
        session.rollback()
    # セッションを閉じる
    session.close()
    return result_json

# assessmentデータ追加
def insert_assessment():
    Session = sessionmaker(bind=engine)
    session = Session()
    # SQLAlchemy ORMを使ったデータ挿入
    new_assessment = assessment(
        assessment_datetime=datetime.now().strftime("%Y%m%d%H%M%S")
    )
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            session.add(new_assessment)
    except sqlalchemy.exc.IntegrityError:
        print("[insert_assessment]一意制約違反によりデータ挿入に失敗しました")
        session.rollback()
    except Exception as e:
        print(f"[insert_assessment]例外が発生しました: {e}")
        session.rollback()
    
    new_assessment_id = new_assessment.assessment_id
    # セッションを閉じる
    session.commit()
    session.close()
    return new_assessment_id

# データ追加(単短レコード)
def myinsert(data_to_insert):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            session.add(data_to_insert)
    except sqlalchemy.exc.IntegrityError:
        print("[myinsert]一意制約違反によりデータ挿入に失敗しました")
        session.rollback()
    except Exception as e:
        print(f"[myinsert]例外が発生しました: {e}")
        session.rollback()
    # セッションを閉じる
    session.commit()
    session.close()
    return 1

# データ追加(複数レコード)
def myinsert_all(data_to_insert):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            session.add_all(data_to_insert)
    except sqlalchemy.exc.IntegrityError:
        print("[myinsert_all]一意制約違反によりデータ挿入に失敗しました")
        session.rollback()
    except Exception as e:
        print(f"[myinsert_all]例外が発生しました: {e}")
        session.rollback()
    # セッションを閉じる
    session.commit()
    session.close()
    return len(data_to_insert)

def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json

def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json

def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = update(mymodel)
    # クエリの内容をターミナルに出力
    print("Parameters:", query.compile().params)  # クエリに渡されるパラメータを出力
    # クエリ実行
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"

def mydelete(mymodel, assessment_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
 
    # セッションを閉じる
    session.close()
    return "delete"