from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    # orm으로 가져와보자!
    articles = Article.objects.all()
    context = {
        'articles' : articles,
    }
    return render(request, 'articles/index.html', context=context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    # form으로 넘긴 데이터를 이런식으로 가져온다
    title = request.POST.get("title")
    content = request.POST.get("content")
    Article.objects.create(title=title, content=content)
    # main 화면으로 redirect
    return redirect('/articles/')