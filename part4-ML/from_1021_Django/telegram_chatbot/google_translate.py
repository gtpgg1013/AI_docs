import requests
from decouple import config

google_key = config("GOOGLE_API_KEY")
api_url = "https://translation.googleapis.com/language/translate/v2"
data ={
    'q': '안녕하세요 쿠쿠입니다 만나서 반가워요!',
    'source': 'ko',
    'target': 'en'
}

# 응답값 json 형태로 받기
response = requests.post(f"{api_url}?key={google_key}", data).json()
print(response)