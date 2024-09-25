from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from jigutime import jigu
import os
import pymysql.cursors
import pytz

app = FastAPI()

@app.get("/")
def test():
    return {"Test": "Done"}

@app.get("/files")
async def file_list():
    conn = pymysql.connect(host='172.17.0.1', port = 53306,
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
    with conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    return result

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    korea = datetime.now(pytz.timezone('Asia/Seoul'))
    request_time = korea.strftime('%Y-%m-%d %H:%M:%S')

    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split('/')[-1]  #"image/png"
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = os.getenv('UPLOAD_DIR', '/home/young12/code/mnist/img')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    import uuid
    ffpath = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')

    with open(ffpath, "wb") as f:
        f.write(img)

    """
    con = pymysql.connect(host="172.17.0.1",
                        port= 53306,
                        user='mnist',
                        password='1234',
                        db='mnistdb',
                        cursorclass=pymysql.cursors.DictCursor)
    """
    sql = "INSERT INTO image_processing (file_name, file_path, request_time, request_user) VALUES (%s, %s, %s, %s)"
    from mnist.db import dml
    insert_row = dml(sql, file_name, ffpath, jigu.now(), "n06")
    #with con:
     #   with con.cursor() as cursor:
      #      cursor.execute(sql, (file_name, ffpath, jigu.now(), "n06"))
       # con.commit()


    # 파일 저장 경로 DB INSERT
    # table name : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가) 
    # 컬럼 정보 : 파일 이름, 파일 경로, 요청 시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측 모델, 예측 결과, 예측 시간(추후 업데이트)

    return {
            "filename": file_name,
            "content_type": file.content_type,
            "file_path": ffpath,
            "insert_row_cont": insert_row
            }

@app.get("/all")
def all():
    # DB 연결 SELECT ALL
    # 결과값 리턴
    from mnist.db import select
    sql = "SELECT * FROM image_processing"
    result = select(query=sql, size=-1)
    return result

@app.get("/one")
def one():
    # DB 연결 SELECT 값 중 하나만 리턴
    # 결과값 리턴
    from mnist.db import select
    sql = """SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size=1)
    return result[0] 

@app.get("/many/")
def many(size: int = -1):
    
    con = pymysql.connect(host="172.17.0.1", 
                        port= 53306,
                        user='mnist',
                        password='1234',
                        db='mnistdb',
                        cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    
    with con:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)
        
    return result
