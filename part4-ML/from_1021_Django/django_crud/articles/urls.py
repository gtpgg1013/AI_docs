from django.urls import path
from . import views

urlpatterns = [
    # 기본 화면이 views.index로 잡혀있네! => views.index 가서 처리 후 => index.html 렌더링 출력
    path('', views.index),
    path('new/', views.new),
    path('create/', views.create),
]