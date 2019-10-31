from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # 만약에 redirect로 그냥 article 인스턴스 call 하면 이 주소가 튀어나감
    def get_absolute_url(self):
        # ex) '/articles/10/'
        return reverse('articles:detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-pk',]

class Comment(models.Model):
    content = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 외래 키
    # 부모 테이블이 지워졌을 때 자식도 따라서 사라져야 함! : on_delete
    # 기존 : article.comment_set.all()
    # 변경 후 : article.comments.all() : related_name을 추가한 후
    # related_name을 추가하면 기존 comment_set 이란 친구를 못 씀!
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    # 순서를 바꿔줄 수 있다 : pk의 역순으로 ordering 해주기!
    class Meta:
        ordering = ['-pk', ]

    def __str__(self):
        return f'<Article({self.article_id}) : Comment({self.pk})-{self.content}>'