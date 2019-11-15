from django.contrib import admin
from .models import Movie, Rating

# Register your models here.
class MoiveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'poster', 'created_at', 'updated_at', 'user')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'score', 'content', 'created_at', 'updated_at', 'user', 'movie')

admin.site.register(Movie, MoiveAdmin)
admin.site.register(Rating, RatingAdmin)