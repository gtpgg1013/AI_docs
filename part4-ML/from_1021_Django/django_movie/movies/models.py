from django.db import models
from django.urls import reverse

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    audience = models.IntegerField()
    open_date = models.DateTimeField()
    genre = models.CharField(max_length=20)
    watch_grade = models.CharField(max_length=20)
    score = models.FloatField()
    poster_url = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass
    
