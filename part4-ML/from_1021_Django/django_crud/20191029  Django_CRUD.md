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