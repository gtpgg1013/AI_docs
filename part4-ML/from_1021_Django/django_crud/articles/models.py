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