from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model

# Create your views here.
def signup(request):

    if request.user.is_authenticated:
        return redirect("movies:index")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("movies:index")
    else:
        form = CustomUserCreationForm()
    context = {'form' : form}
    return render(request, 'accounts/auth_form.html', context)
            
def login(request):
    if request.user.is_authenticated:
        return redirect("movies:index")
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or "movies:index")
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect("movies:index")

@require_POST
def delete(request):
    request.user.delete()
    return redirect("movies:index")

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("movies:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("movies:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)

def profile(request):
    person = get_object_or_404(get_user_model())
    context = {'person':person}
    return render(request, 'accounts/profile.html', context)
