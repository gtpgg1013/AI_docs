from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'key' : 'value'
    }
    return render(request, 'pages/index.html', context)