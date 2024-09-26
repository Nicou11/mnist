import os
import requests

def send_line_noti(file_name, presult):
    api = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTI_TOKEN', 'NULL')
    h = {'Authorization':'Bearer ' + 'Emmxfqz6116i2EA0qiw6upL0OM5MD5TjjvMczK3a9hg'}
    msg = {
       "message" : f"{file_name} => {presult}"
    }
    response = requests.post(api, headers=h , data=msg)
    print(response.text)
    print("SEND LINE NOTI")



send_line_noti('filename', 'result')
