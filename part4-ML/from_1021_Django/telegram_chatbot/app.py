from decouple import config
from flask import Flask, render_template, request, jsonify
import requests
import random
app = Flask(__name__)

# token 변수 설정 후 api url 설정
token = config("TOKEN")  # .env에 들어있는 TOKEN이라는 변수 가져오는 함수
google_key = config("GOOGLE_API_KEY")
google_url = "https://translation.googleapis.com/language/translate/v2"

api_url = f"https://api.telegram.org/bot{token}"
update_url = f"{api_url}/getUpdates"

# getUpdate Json file에서 chat_id 값 꺼내기
# response = requests.get(update_url).json()
# chat_id = response["result"][0]["message"]["chat"]["id"]

# 메세지에 로또 번호 6개 뽑아서 보내주기
# message = random.sample(range(1,46), 6)

@app.route('/')
def root():
    return render_template('write.html')

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    message = request.args.get('message')
    message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(message_url)
    return render_template('write.html')

# 이 또한 결국 post 방식으로 telegram server에 api key를 떤져주면 그에 상응하는 일을 알아서 해주는 것!
@app.route(f'/{token}', methods=["POST"])
def telegram():
    message = request.get_json() # 현재 페이지 => 즉, webhook 페이지
    # print(message)
    # chat_id 가져오기
    # chat_id = message["message"]["chat"]["id"]
    # telegram에서 보낸 메시지 꺼내기
    # text = message["message"]["text"]
    # 메시지를 보내는 요청 주소를 통해 텔레그램에 전달
    # message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={text}"
    # get방식으로 보낸 것?
    # requests.get(message_url)

    # 이 밑의 message는 dialogflow를 통해 들어온 jsonfile이어서 parsing을 새로 해줘야 함!
    dialog_flow = message["originalDetectIntentRequest"]["payload"]
    text = dialog_flow["text"]
    # chat_id = dialog_flow["chat"]["id"]

    if text[0:3]=="/로또":
        reply = random.sample(range(1,46),6)
        reply = ' '.join(str(reply))
    elif text[0:3]=="/번역":
        data = {
            'q':text[4:],
            'source':'ko',
            'target':'en'
        }
        response = requests.post(f"{google_url}?key={google_key}", data).json()
        reply = response["data"]["translations"][0]["translatedText"]
    elif text[0:3]=="/에코":
        reply = text[4:]
    elif text[0:5]=="/help":
        reply = """
                /에코 : 메아리치기
                /로또 : 로또번호
                /번역 + 번역문장 : 한->영 번역
                """
    else:
        # None을 return으로 던져주면 알아서 dialogflow 선에서 처리하여 대답해줌!
        reply = None

    result = {'fulfillmentText':reply}
    # 즉, api + method + 등의 인자를 get 방식으로 날려주면 chatbot server에서 상응하는 액션을 취해줌! 
    # message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={reply}"
    # requests.get(message_url)
    # print(message)
    # print(result)
    # print(token)
    return jsonify(result)
    # 이게 어디로 갈까? => dialogflow를 거쳐서 telegram으로 출력!

if __name__=="__main__":
    app.run(debug=True)

# message_url = f"{api_url}/sendMessage?chat_id={chat_id}&text={message}"
# requests.get(message_url)