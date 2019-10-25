# 20191025 Django Intro

폴더 만들고 => venv 생성 => venv 생성 => django-admin startproject django_intro . (장고 프로젝트 시작)

settings.py => django 모든 세팅

- 언어 / 시간 설정 가능

urls.py => 들어올 url 경로 설정

wsgi.py => 배포할 때 사용할 파일

manage.py => 장고 프로젝트 관련 모든 파일 관리하는 파일 => 함부로 건들지 마라



- 서버 시동 => python manage.py runserver
- 여러개의 앱으로 구성
  - python manage.py startapp pages : pages라는 새로운 앱 생성
  - admin.py => 관리자 계정
  - models.py => db모델 스키마 클래스 형태 작성 가능
  - tests.py => test코드 작성 / 할때 : 질문사항 => Django TDD
  - views.py => url 들어오면 그에대한 처리
  - 앱 만들고 장고 서버 settings에가서 app 추가해줘야함 => installed_apps
  - 그리고 그 추가된 views에 index 함수 추가해주고 : 걔가 template 폴더에 있는 html 파일 가져와줌



- 앱 만들고 => 세팅(project)에 추가하고 => 앱에 관련된 함수(라우팅)를 뷰에 써주고 => url(project)에 경로 추가