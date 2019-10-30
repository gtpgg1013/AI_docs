from django.shortcuts import render, redirect
from .models import Student

# Create your views here.
def index(request):
    # orm에서 가져오기
    students = Student.objects.all()
    context = {
        'students' : students
    }
    return render(request, 'students/index.html', context)

def new(request):
    return render(request, 'students/new.html')

def create(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    birthday = request.POST.get("birthday")
    age = request.POST.get("age")
    Student.objects.create(name=name, email=email, birthday=birthday, age=age)
    return redirect('/students/')