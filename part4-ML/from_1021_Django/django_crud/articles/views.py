from django.shortcuts import render, redirect
from .models import Article
import datetime

# Create your views here.
def index(request):
    # orm으로 가져와보자!
    articles = Article.objects.all()
    context = {
        'articles' : articles,
    }
    return render(request, 'articles/index.html', context=context)

# def new(request):
#     return render(request, 'articles/new.html')

# 분기를 넣어주자!
def create(request):
    if request.method == "POST":
        # form으로 넘긴 데이터를 이런식으로 가져온다
        title = request.POST.get("title")
        content = request.POST.get("content")
        article = Article.objects.create(title=title, content=content)
        # main 화면으로 redirect
        return redirect('articles:detail', article.pk)
    else: # GET방식
        return render(request, 'articles/new.html')

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {'article' : article}
    return render(request, 'articles/detail.html', context)

def delete(request, pk):
    if request.method == "POST":
        article = Article.objects.get(pk=pk)
        article.delete()
        return redirect('articles:index')
    else:
        # return redirect('articles:detail',article.pk)
        return redirect(article)

# def edit(request, pk):
#     article = Article.objects.get(pk=pk)
#     context = {'article' : article}
#     return render(request, 'articles/edit.html', context)

def update(request, pk):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        article = Article.objects.get(pk=pk)
        article.title = title
        article.content = content
        # article.updated_at = datetime.datetime.now()
        # 얘는 알아서 DB를 hit 할때마다 갱신됨!
        article.save()
        return redirect('articles:index')
    else:
        article = Article.objects.get(pk=pk)
        context = {'article' : article}
        return render(request, 'articles/update.html', context)