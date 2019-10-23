# 2019/10/23 : Telegram chatbot

### 환경 설정

venv 걍 키면 좋고

library : python-decouple(.env의 config된 변수들 쓰기 위해) / requests(웹 데이터 가져오기)





### API

일단 telegram을 깔고, BotFather를 선택

/newbot : 새 bot 만들기

bot 이름(local 이름) 설정 / bot이름(global 이름) 설정

api key 받아서 .env에 token으로 저장

**ngrok** 

​	https://dashboard.ngrok.com/get-started : 다운받아서 exe 파일 넣어주고, connect account : 코드 복붙(홈페이지에서)

​	./ngrok http 5000 : local server에 5000 port open : cmd창에서 해줘야 할 수도 있음 / git bash는 안될 때도 있음

​	그리고 이 cmd창을 보면 forwarding 해주는 주소가 있음을 확인할 수 있음 => 복사해서 setwebhook에 넣어주기



### 실제 개발

flask server를 만들어서 거기서 데이터를 보냈을 때 telegram으로 그 메시지를 받을 수 있게 하기

web hook? : telegram과 flask, user가 interaction 할 수 있게 해줌

웹 훅은 한번만 걸어주면 되기 때문에, 별도의 파일로 분리해서 관리 : set_webhook.py

ngrok으로 local server 오픈해주기! 

​	setWebhook : 위의 내용대로 따라해주쇼

Dialogflow : 챗봇 서비스 ! : intents => 화자의 의도 : training pharse 여러개 넣어주면 학습



dialogflow : Intents에 성향들 설정 / entities로 집합 설정 / integrations에 telegram 토큰 넣어주고 start



이게 telegram에서 요청 보내면 flask로 가야하는데, dialogflow로 가고있다 => fullfillment 탭 설정

호스팅된 주소 + telegram token (webhook 주소) 를 넣어주



Default Welcome Intent => 맨 밑 fullfillment : enable하게 설정





### Insight

- 그러면 어찌되었건 GET / POST 방식으로 통신을 하는데, 그에 대한 결과는 그럼 서버가 결정하는 것? : API 문서에 보면 어떤 걸 돌려준다! 라고 써 있는것인가?
- dialogflow의 데이터 처리 순서
  - telegram의 api 주소의 웹훅을 dialogflow에 걸어놔줬음
    - 원래는 flask가 처리해서 떤져줬는데
    - 이렇게 해놓으면 그 웹훅을 땡겨서 dialogflow가 쓴다
    - 타이밍이 이상하다???
    - 맨 처음 telegram => dialogflow => flask => dialogflow => telegram 순으로 돌아옴!
      - 아하 맨 마지막에 다시 dialogflow를 거쳐서 telegram으로 출력하기 때문에 만약 fallback이나 welcome defalut value가 들어오게 되면 dialogflow에서 처리해서 내보내기 때문에 더 좋다!
- pythonanywhere로 간단히 배포 가능!
- 걍 파일 간단히 때려 넣고 / 필요한 library 설치 (pip3 install --user python-decouple)
- web hook을 새로 걸어줘야함!
  - https://gtpgg1013.pythonanywhere.com/579225036:AAE1hFV4S_CCIWmQsTVMYHG5IVLeLA1iLTY
  - set_webhook.py에 위 주소를 setWebhook url 새 설정해주고 실행!
  - 그리고 dilogflow의 fulfillment의 webhook또한 걸어줘야 함!