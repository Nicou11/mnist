from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors

app = FastAPI()

@app.get("/")
def test():
    return {"Test": "Done"}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "./photo"
    ffpath = os.path.join(upload_dir, file_name)

    import pymysql.cursors

    connection = pymysql.connect(host=os.getenv("DB_IP", "localhost"),
                        port= int(os.getenv("DB_PORT", "33306")),
                        user='mnist',
                        password='1234',
                        db='mnistdb',
                        cursorclass=pymysql.cursors.DictCursor)

    sql = "INSERT INTO image_processing (file_name, content_type, dt) VALUES (%s, %s, %s)"

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (file_name, content_type, real_time))
        connection.commit()

    with open(ffpath, "wb") as f:
        f.write(img)

    # 파일 저장 경로 DB INSERT
    # table name : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가) 
    # 컬럼 정보 : 파일 이름, 파일 경로, 요청 시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측 모델, 예측 결과, 예측 시간(추후 업데이트)

    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": ffpath,
            }
