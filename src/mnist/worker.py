from jigutime import jigu
from mnist.db import get_conn, select, dml
import os
import requests
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from mnist.model.manager import get_keras_path

def get_job_img_task():
    sql = """
    SELECT num, file_name, file_path
    FROM image_processing 
    WHERE prediction_result IS NULL
    ORDER BY num -- 가장 오래된 요청
    LIMIT 1 -- 하나씩
    """
    r = select(sql, 1)

    if len(r) > 0:
        return r[0]
    else:
        return None

#model_path = get_keras_path()
model = load_model(get_keras_path()) # 학습된 모델 파일 경로

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    img = 255 - np.array(img)  # 흑백 반전
    
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit


def prediction(file_path, num):
    sql = """UPDATE image_processing
    SET prediction_result=%s,
        prediction_model='n06',
        prediction_time=%s
    WHERE num=%s
    """
    #file_path = '/home/young12/code/mnist/img/test_2.png'
    
    presult = predict_digit(file_path)
    dml(sql, presult, jigu.now(), num)
    print(f"파일 {os.path.basename(file_path)}의 예측된 숫자: {presult}")
    return presult 

def run():
  #"""image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  # STEP 1
  # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 가져오기
    job = get_job_img_task()

    if job is None:
        print(f"{jigu.now()} - job is None")
        return  

    num = job['num']
    file_name = job['file_name']
    file_path = job['file_path']
  # STEP 2
  # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
  # 동시에 prediction_model, prediction_time 도 업데이트
    presult = prediction(file_path, num)
  # STEP 3
  # LINE 으로 처리 결과 전송
    send_line_noti(file_name, presult)
    print(jigu.now())

def send_line_noti(file_name, presult):
    api = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_KEY', 'NULL')
    h = {'Authorization':'Bearer ' + token}
    msg = {
       "message" : f"{file_name} => {presult}"
    }
    response = requests.post(api, headers=h , data=msg)
    print("SEND LINE NOTI")

#prediction('/home/young12/code/mnist/img/test_2.png', 1)
