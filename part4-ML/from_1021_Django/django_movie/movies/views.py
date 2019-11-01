from django.shortcuts import render, redirect
from .models import Movies

# Create your views here.
def index(request):
    movies = Movies.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/index.html', context)

def new(request):
    return render(request, 'movies/new.html')

def create(request):
    movie = Movies()
    movie.title = request.POST.get("title")
    movie.title_en = request.POST.get("title_en")
    movie.audience = request.POST.get("audience")
    movie.open_date = request.POST.get("open_date")
    movie.genre = request.POST.get("genre")
    movie.watch_grade = request.POST.get("watch_grade")
    movie.score = request.POST.get("score")
    movie.poster_url = request.POST.get("poster_url")
    movie.description = request.POST.get("description")
    movie.save()
    return redirect('movies:detail', movie.pk)

def detail(request, pk):
    movie = Movies.objects.get(pk=pk)
    # print(type(movie.open_date))
    context = {
        'movie' : movie
    }
    return render(request, 'movies/detail.html', context)
    
def edit(request, pk):
    movie = Movies.objects.get(pk=pk)
    if request.method == "POST":
        context = {
            'movie' : movie
        }
        return render(request, 'movies/edit.html', context)
    else:
        return redirect('movies:detail', movie.pk)

def update(request, pk):
    movie = Movies.objects.get(pk=pk)
    if request.method == "POST":
        movie.title = request.POST.get("title")
        movie.title_en = request.POST.get("title_en")
        movie.audience = request.POST.get("audience")
        movie.open_date = request.POST.get("open_date")
        movie.genre = request.POST.get("genre")
        movie.watch_grade = request.POST.get("watch_grade")
        movie.score = request.POST.get("score")
        movie.poster_url = request.POST.get("poster_url")
        movie.description = request.POST.get("description")
        movie.save()
        return redirect('movies:detail', movie.pk)
    else:
        return redirect('movies:detail', movie.pk)

def delete(request, pk):
    if request.method == "POST":
        movie = Movies.objects.get(pk=pk)
        movie.delete()
    else:
        pass
    return redirect('movies:index')