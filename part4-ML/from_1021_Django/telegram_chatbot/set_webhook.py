# set_webhook.py
# 웹 훅은 한번만 걸어주면 되기 때문에, 별도의 파일로 분리해서 관리
from decouple import config
import requests

# 이걸 통해서 telegram이 무슨 일이 일어나면 POST로 flask server에 log를 남김
token = config("TOKEN")
api_url = f"https://api.telegram.org/bot{token}"
# set_webhook_url = f"{api_url}/setWebhook?url=https://4de94fa9.ngrok.io/{token}"
set_webhook_url = f"{api_url}/setWebhook?url=https://gtpgg1013.pythonanywhere.com/579225036:AAE1hFV4S_CCIWmQsTVMYHG5IVLeLA1iLTY"
# https://4de94fa9.ngrok.io/579225036:AAE1hFV4S_CCIWmQsTVMYHG5IVLeLA1iLTY

response = requests.get(set_webhook_url)
print(response.text)