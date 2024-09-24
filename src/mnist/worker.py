from jigutime import jigu
from mnist.db import get_conn, select, dml


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

def prediction(file_path, num):
    sql = """UPDATE image_processing
    SET prediction_result=%s,
        prediction_model='n06',
        prediction_time=%s
    WHERE num=%s
    """
    import random

    presult = random.randint(0, 9)
    dml(sql, presult, jigu.now(), num)
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

