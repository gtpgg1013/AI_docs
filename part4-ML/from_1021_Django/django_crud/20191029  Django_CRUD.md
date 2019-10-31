# 2019/10/29 : Django_CRUD

가상환경 생성

프로젝트 생성 : django-admin startproject crud .

앱 생성 : python manage.py startapp articles

articles에 templates/articles 라는 산하 폴더 생성 

crud에 templates 라는 산하 폴더 생성

그리고 setting.py <= dirs 수정해주는 이유 : crud 밑의 template는 원래 django가 못찾아다녀서, 여기도 보세요~ 해주는 것

APP_DIRS = True 하면 app들 밑의 templates 폴더를 찾아다님

프로젝트 / 앱에 각각 템플릿 폴더를 만들어주고, 

프로젝트의 urls로부터 각 앱으로 url 배분(include 사용)

그리고 각 앱에서 실제 url 패턴을 사용

setting.py에서 TEMPLATES에 DIRS에 경로 추가 crud tempaltes 왜?

그리고 그 밑에 views랑 html파일 제작



python manage.py makemigrations : 모델의 설계도 만들기!

python manage.py migrate : 실제 migrate!



migrate 후 admin.py에서 어드민 관련 코드 작성후

python manage.py createsuperuser

그리고 admin에서 내용 확인 가-능



GET과 POST

- GET은 데이터를 가져오는 READ
- POST는 데이터를 서버에 던지는 CREATE





# Day 2

### 각 게시글에 대한 세부 페이지 구성!



Update는 두가지 스텝으로

- 원래 데이터 가져와서 보여주고
- 다시 수정에서 DB에 넣어줌



#### 내가 이해한 기본 로직

- urls.py가 가장 먼저 동작! (들어가자 마자 root page 보여주니까)
- 그리고 그 url로 들어가면서 views에 정의된 함수로 이동!
- views에서 정의된 함수가 실행되고 보통 html파일을 렌더링함
- 반복
- 그 외에 특정 task를 수행하는 url은 redirect



추가 : views에서 사용되는 메소드들의 인자값은 url의 꺾새로부터 들어옴!

추가 2 : delete나 update같은 작업은 POST로 작업해야 하므로 form tag : method=POST 활용!



#### 실습

students라는 새로운 app 만들기

모델 만들고 (DB 스키마)

마이그레이션하고

어드민 만들고

setting에서 app 추가하고

crud의 urls에서 url 추가하고 / students의 url에 추가 (urls.py 만들어)

template도 만들어야지

django.urls의 path는 뭐하는 애지?



python manage.py makemigrations : 모델의 설계도 만들기!

python manage.py migrate : 실제 migrate!



request 객체는 사용자가 요청한 정보 일체를 담고있는 객체!

- request
- request.path
- request.method
- request.headers
- request.GET
- request.POST



onclick : 하면 할 수 있슴!



그리고 url 자체가 바뀌게 되었을 때 만약 전부다 손으로 써놓은 거라면

=> 고치는 건 거의 불가능! : 그래서 각 url마다 pagename을 붙여준다

urls.py 맨 위에 app_name 지정해주고

그리고 app_name:pagename 같은 식으로 접근하면 참 조타!

**form action="{% url 'articles:edit_processing' article.pk %}" method="POST"**

이런식으로 하면 됨!



RESTful API

- 자원 : resource
- 행위 : method
- 표현 : presentation

자체 표현구조 (Self-descriptiveness) : URI 자체로 표현할 수 있어야 함!



Rest 중심규칙

- URI는 정보의 자원

- 자원에 대한 행위는 HTTP Method로 표현한다! 
- GET /users/1/read/ : 이같은 예시는 사실 RESTful하지 않다!
- GET /users/1/ : 이게 RESTful!



- '행위'에 대한 내용이 중복되지 않게 하는 게 첫번째 point일 듯



리소소를 표현하는 Collection과 Document!



Beautify : VS code extension

깔고 전체 선택 후 f1 Beautify 하면 이쁘게 들여쓰기 함



# Day 3

faker 패키지를 이용한 재밌는 앱

jobs라는 새로운 앱 만들기 : python manage.py startapp jobs



### 데이터베이스!

Article과 Comment 두개의 테이블이 있을 때 두 테이블을 어떻게 연결하니?

​	comment table에서 참조할 부모 테이블의 정보를 알기 위해 article의 pk를 fk로 받음

​	Primary key & Foriegn key

​	one to many 관계!

​	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

위와 같이 설정해주면 article 객체를 ORM으로 땡겨왔을 때 그와 연결된 comments를 models.ForeignKey(...) 로 가져올 수 있다

그리고 그 가져온 쿼리 리스트를 for문돌려서 하나씩 꺼내오면 됨!

migration



python manage.py shell_plus

여기에서 testing 가능



ORM을 이용한 PK FK 사용법!



pip freeze > requirements.txt 로 dependency library 저장

