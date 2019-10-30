from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # 기본 화면이 views.index로 잡혀있네! => views.index 가서 처리 후 => index.html 렌더링 출력
    # 각 path에다가 이름을 지어줄 수 있음! => 만약 실제 url 바뀔때 다 따라다리면서 바꾸기 힘들다!

    # 기존 url
    # path('', views.index, name='index'),
    # path('new/', views.new, name='new'),
    # path('create/', views.create, name='create'),
    # path('<int:pk>/', views.detail, name='detail'), # 특정 게시글로 가야하니까!
    # path('<int:pk>/delete/', views.delete, name='delete'),
    # path('<int:pk>/edit/', views.edit, name='edit'),
    # path('<int:pk>/edit_processing/', views.edit_processing, name='edit_processing')

    # 변경 후 url : RESTful하게
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/update/', views.update, name="update")
]
