from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from IPython import embed

# Create your views here.
def index(request):
    # embed()
    articles = Article.objects.all()
    context = {'articles' : articles}
    return render(request, 'articles/index.html', context)

# @login_required(login_url="/accounts/test") 이런식으로도 사용 가능!
@login_required
def create(request):
    # embed()
    if request.method == "POST":
        # 폼 인스턴스를 생성하고 요청에 의한 데이터로 채운다. (binding)
        form = ArticleForm(request.POST)
        # embed()
        # 폼이 유효한지 체크한다.
        if form.is_valid():
            # modelform을 써서 가능! => 바로 save 가능
            # article = form.save()
            # 이 밑에를 써줘야 article에 현재 로그인된 user가 들어감!
            article = form.save(commit=False) # commit=False로 데려오면 객체로 쓸 수 있다!
            article.user = request.user
            article.save()
            # title = form.cleaned_data.get("title")
            # content = form.cleaned_data.get("content")
            # article = Article(title=title, content=content)
            # article.save()
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm()
        context = {'form': form }
    return render(request, 'articles/create.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    comments = Comment.objects.filter(article=article_pk)
    # embed()
    context = {
        'article':article, 
        'comment_form':comment_form,
        'comments':comments
        }

    # 위 코드는 아래와 동일
    # try:
    #     article = Article.objects.get(pk=article_pk)
    # except Article.DoesNotExist:
    #     # from django.http import Http404
    #     raise Http404("No article matches the given query.")

    # context = {'article': article}
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
        return redirect("articles:index")
    else:
        return HttpResponse("You are Unauthorized", status=401)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article.title = form.cleaned_data.get("title")
                article.content = form.cleaned_data.get("content")
                article.save()
                return redirect("articles:detail", article_pk)
        else:
            form = ArticleForm(
                instance=article
            )
    else:
        return redirect("articles:index")
    context = {'form' : form}
    return render(request, 'articles/create.html', context)

# @login_required랑 같이 쓸수 없어서 request.user.is_authenticated를 써줌! (redirect가 get요청이라서 같이 못씀)
@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # forien key로 model을 가져왔으므로, 얘도 model 객체를 가져와야 함!
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect("articles:detail", article_pk)
    else:
        return HttpResponse("You are Unauthorized", status=401)

@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect("articles:detail", article_pk)
    else:
        return redirect("accounts:login")
        # return HttpResponse("You are Unauthorized", status=401)
