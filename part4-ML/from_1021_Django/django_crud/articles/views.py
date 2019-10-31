from django.shortcuts import render, redirect
from .models import Article, Comment
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
    comments = article.comments.all()
    context = {'article' : article, 'comments' : comments}
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

# 버그 났던 이유 : 항상 어디선가 요청하면(html) => urls.py => views.py => 다시 html 파일 임을 기억하자!
def comment_create(request, pk):
    aritcle = Article.objects.get(pk=pk)
    if request.method == "POST":
        # request에서 얻어올 때 : request 객체의 내용을 확실히 알아야 좋다!
        content = request.POST.get("content")
        comment = Comment()
        comment.content = content
        comment.article = aritcle
        comment.save()
    else:
        pass
        # models.py에 정의해 놓은 get_absolute_url 함수를 정의하니 OK!
        # return redirect("articles:detail", article.pk)
    return redirect(aritcle)

def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # a_pk = comment.comment_id # 이렇게 하면 더 복잡한가?
    article = Article.objects.get(pk=article_pk)
    # article = Article.objects.get(pk=a_pk)
    if request.method == "POST":
        comment.delete()
    return redirect('articles:detail', article.pk)