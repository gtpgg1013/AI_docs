from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Rating
from .forms import MovieForm, RatingForm
from django.contrib.auth.decorators import login_required
from IPython import embed
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import numpy as np
from django.db.models import Avg

# Create your views here.
def index(request):
    # movies = Movie.objects.all()
    movies = Movie.objects.annotate(avg_score=Avg('rating__score')) # annotate : 주석을 단다! 
    # groupby연산을 한 놈을 model에 포함시켜 가져가기 => 기본적 쿼리는 다 가져감!
    # movie.avg_score
    context = {'movies':movies}
    return render(request, "movies/index.html", context)

def new(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES) # 그냥 인자를 두개 때려넣어주면 됨!
        # form.poster = request.FILES.get("poster") # 이렇게는 안씀!
        # embed()
        print(form)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
        return redirect("movies:index")
    else:
        form = MovieForm()
        context = {'form' : form}
    return render(request, 'movies/new.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating_form = RatingForm()
    ratings = Rating.objects.filter(movie=movie)
    scores = []
    for rating in ratings:
        scores.append(float(rating.score))
    # embed()
    mean_val = np.mean(scores)

    context = {
        'movie': movie,
        'rating_form':rating_form,
        'mean_val':mean_val,
        }

    return render(request, 'movies/detail.html', context)

def edit(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user == movie.user:
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                movie.title = form.cleaned_data.get("title")
                movie.description = form.cleaned_data.get("description")
                movie.poster = form.cleaned_data.get("poster")
                movie.save()
            return redirect("movies:index")
        else:
            form = MovieForm(instance=movie)
            context = {'form': form}
    return render(request, 'movies/new.html', context)

@require_POST
def delete(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.user == movie.user:
            movie.poster.delete()
            movie.delete()
    return redirect("movies:index")
    
@require_POST
def new_rating(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.movie = movie
            rating.user = request.user
            rating.save()
        return redirect("movies:detail", movie_pk)
    else:
        return HttpResponse("UNAUTHORIZED", status=401)

@require_POST
def delete_rating(request, movie_pk, rating_pk):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, pk=rating_pk)
        if rating.user == request.user:
            rating.delete()
        return redirect("movies:detail", movie_pk)
    else:
        return redirect("accounts:login")