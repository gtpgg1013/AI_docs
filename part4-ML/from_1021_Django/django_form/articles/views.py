from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST, require_GET
from IPython import embed

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {'articles' : articles}
    return render(request, 'articles/index.html', context)

def create(request):
    # embed()
    if request.method == "POST":
        # 폼 인스턴스를 생성하고 요청에 의한 데이터로 채운다. (binding)
        form = ArticleForm(request.POST)
        # embed()
        # 폼이 유효한지 체크한다.
        if form.is_valid():
            # modelform을 써서 가능! => 바로 save 가능
            article = form.save()
            # title = form.cleaned_data.get("title")
            # content = form.cleaned_data.get("content")
            # article = Article(title=title, content=content)
            # article.save()
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm()
        context = {'form': form}
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
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect("articles:index")

def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
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
    context = {'form' : form}
    return render(request, 'articles/create.html', context)

@require_POST
def comments_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        # forien key로 model을 가져왔으므로, 얘도 model 객체를 가져와야 함!
        comment.article = article
        comment.save()
    return redirect("articles:detail", article_pk)

@require_POST
def comments_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", article_pk)