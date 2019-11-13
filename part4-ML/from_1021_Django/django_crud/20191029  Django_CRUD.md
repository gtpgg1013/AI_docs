# 2019/10/29 : Django_CRUD

가상환경 생성

 pip install -r requirements.txt 

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



datetime format을 불러와서 그대로 수정할 때

**input type="date" name="open_date" value="{{ movie.open_date|date:'Y-m-d' }}"**

이런식의 | 기호를 사용하는 포맷지정이 필요하다





# Day 4

ipython 으로 embed로 interactive하게 디버깅 가능

request는 그냥 계속 꼭 안넘겨줘도 떤져주잖아~

bootstrap4 : 라이브러리 설치

### Form도 forms.py로 ORM처럼 미리 틀을 만들어서 사용할 수 있다!

Articleform(modelform)

modelform => DB랑 form을 한방에 해주는 객체!

create 수정 : request.resolver_match : 세부 정보



Comment도 이와 같은 방법으로 추가해주기

=> migration



Model.objects.get() : 쓰면 존재하지 않을경우 error

Model.objects.filter: 쓰면 없으면 빈 쿼리



{% for comment in article.comment_set.all %}

comment를 안넘겨주고도 가져올 수 있다!

- 이 comment_set 이란 것은 : foriegn key를 지정해줄 때 알아서 만들어주는 객체! 이걸로 관련된 애들 set가져올 수 있다

{% for comment in comments %}



데코레이터!

from django.views.decorators.http import require_POST

@require_POST

이놈을 view함수 위에 써주면 그놈은 POST만 받을 수 있음!

만약 이놈을 그냥 GET으로 접근하면 405 Error!



form을 써서 좋은점 : 모델을 보고 고대로 그 형식 고대로 폼을 만들어줌 => 그리고 그 폼 객체에 정보를 담든 안담든 해서

그놈을 그대로 인자로 template로 넘겨주면 {{ }} 형식으로 그대로 쓸 수 있다



# 유저 관련기능 : AUTH

유저관련기능 모델폼은 이미 만들어놓음!

로그인 : session create!

로그아웃 : session delete!



로그인 후 글쓰게 만들고 싶다 => 

from django.contrib.auth.decorators import login_required

@login_required 데코레이터 사용하면 됨!



로그인 안하고 url로 접근하려 하면

 http://127.0.0.1:8000/accounts/login/?next=/articles/create/ 

요거는 로그인 수행하면 next쿼리의 인자로 이동시켜주겠다는뜻!



쿠키

세션



auth_login(request, form.get_user())

form.get_user() 는 user_cache(정제된 데이터)를 return

결과적으로 user의 객체를 가져오게 됨



나쁘지않은 css  https://materializecss.com/ (부트스트랩처럼 쓰면 됨)



dir(request.user)

이거 쓰면 request.user의 변수들 알 수 있음 / is_authenticated 등등..



@login_required

@require_POST

두개를 같이 쓸 수 없음!

왜 같이 못쓰누? 

login_required가 던져주는 redirect가 get방식이어서

@require_POST 데커레이터에 걸려서 405에러(Method error)가 남!



User : Article의 관계?

1 : N ? / M : N ? 



article의 model.py에서

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

를 추가해주면 : user를 foreign key로 가져옴!

근데 밑에를 보면 article = models.ForeignKey(Article, on_delete=models.CASCADE)

로 가져올 수 있으!

결국 models.ForeignKey()의 첫번째 인자로 string, object 두개 다 데려올 수 있으나, 맨 처음 장고가 실행되면 settings에 정의된 installed_APP 순서대로 app을 실행하는데, 거기에서 get_user_model()을 사용하면 로드가 안되서 에러가 남 => settings.AUTH_USER_MODEL 사용!



article에 user 외래 키로 주고 makemigrations 하자! => 오류메시지나면 1번 선택

그리고 1이라고 쳐주면 지금까지 써있던 글들의 외래 키가 1로 됨(user 1)

migrate gogo



# 놓친 부분

gravatar

card로 내용 부분 대체하기

password hassing

좋아요

M : N



# M : N

다양한 데이터베이스의 표현을 위해

중개 테이블을 만들어서 표현

어떻게든 관계를 테이블 위에 적어야 하는데 그렇게 안될 때가 있음 : 환자 / 의사 관계!

중개 테이블로 그 관계들을 끌고온다

#### 중개 테이블 있을 시 : Reservation table을 만들었을 경우

doctor1.reservation_set.all()

patients1.reservation_set.all()

#### Django는 manytomany field를 함수로 제공

patient1.doctors.all()

doctor.patient_set.all() # related_name을 ManyToManyField로 바꿔주면 patient_set을 그 이름으로 바꾸기 가능

#### 그냥 데이터를 가져오기만 할 때는 ManyToMany로 가능

#### 만약 추가 데이터가 더 필요하다면 중개 모델이 필요함! (Ex.예약 시간)



migration 작업 하셈



sqlite 라는 extension 깔면 sqlite DB를 시각화해서 더 편하게 볼 수 있음!

many to many 는 일단 가상환경만 딱 깔아놓은 상태



TDD?

test - driven development

pip install django_test_plus



draw.io => UML



걍 폰트어섬에서 가져와서 head에다 script 박고 쓰면 됨

=> 이것도 일종의 css library! => class로 가져오면 됨!



#### User models customizing

AUTH_USER_MODEL = 'accounts.User' 이걸를 써줘야함

유저모델을 먼저 해줘야함!!! => 안그러면 다 날려야함

db 날리고 articles의 migration 다 날려야 함



migrations folder가 안날라가게 조심하여야 함!



User를 custom으로 만들었으면 user를 건드는 form도 custom하게 써줘야 함!



get_user_model : 현재 user의 model!



custom filter를 만들어서 할 수도 있다! => templatetags! : make_links

## {{ article|hashtag_link|safe }}

이렇게 하면 django가 escaping하는 걸 그냥 막아줌! : a태그가 걸리게 됨



### pip install django-allauth

다른 provider들의 auth 기능 가져와서 쓰기!

INSTALLED_APPS

AUTHENTICATION_BACKENDS

두개 변수 추가!



 https://django-allauth.readthedocs.io/en/latest/installation.html 



project의 url에 추가

  path('accounts/', include('allauth.urls')),



카카오 auth : 앱 만들고

**설정 - 일반 - 플랫폼 - 플랫폼 추가**

http https : 127 로컬호스트 추가

**설정 -  사용자관리 : on**

프로필 정보 on / 카카오계정 (이메일) on



### 공식문서

## Kakao

- App registration (get your key here)

  https://developers.kakao.com/apps

- Development callback URL

  http://127.0,0,1:8000/accounts/kakao/login/callback/



http://127.0,0,1:8000/accounts/kakao/login/callback/

요거를 로그인 redirect uri 에 추가해 줘야 함

글구 login.html로 바꿀거임(종전 auth_form.html로 공유하고 있었음)



이 밑에처럼 login.html에 추가

<a href="{% provider_login_url 'kakao' %}" class="btn btn-warning">카카오 로그인</a



어드민가서 소셜 어플리케이션 추가해야 함!

클라이언트 아이디 : REST API

비밀키 : 고급에서 비밀 키 발급



장고 사이트에 127.0.0.1:8000 도메인명 표시명 추가



제대로 된 리디렉션 잡아주기!

default => /accounts/profile/ 인데 현재 다르게 쓰고있음! <username> 으로

LOGIN_REDIRECT_URL = 'articles:index'