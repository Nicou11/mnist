import numpy as np
from PIL import Image
from keras.models import load_model

# 모델 로드
model = load_model('mnist240924.keras')  # 학습된 모델 파일 경로

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

# 예측
def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit

# 사용자 이미지 경로
image_path = '/home/diginori/code/samdul77food/note/555.png'

# 예측 실행
predicted_digit = predict_digit(image_path)
print("예측된 숫자:", predicted_digit)
