from django.shortcuts import render
from faker import Faker
from .models import Job
import requests
from decouple import config

# Create your views here.
def index(request):
    return render(request, 'jobs/index.html')

# 이 상황에서 숫자를 여러개 만드는 게 나은가 아니면 이게 나은가?
# 보통 어느쪽이 최적화
def past_life(request):
    name = request.POST.get("name")
    
    # db에 이름이 있는지 확인!
    person = Job.objects.filter(name=name).first()

    # job.objects.filter(name=name).query : 쿼리 확인 가능
    # filter를 쓰면 만약에 비어있어도 에러가 안나기 때문에 (빈 쿼리셋) : 쓰기 편함
    # db에 이미 같은 name이 있으면 기존 name의 past_job을 가져오기!

    # get은 만약 값이 없으면 error
    # try:
    #     person = Job.objects.get(name=name)
    #     past_life_job = person[1]
    # except:
    #     person = None

    # 없으면 db에 저장한 후 가져오기

    if not person:
        fake = Faker()
        past_job = fake.job()
        person = Job(name=name, past_job=past_job)
        person.save()
    else:
        past_job = person.past_job

    GIPHY_API_KEY = config("GIPHY_API_KEY")
    url = f'http://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={past_job}&limit=1'
    print(url)
    data = requests.get(url).json()
    # 이것도 만약 dictionary식으로 계속해서 들어갔을 때, 없으면 에러발생!
    image = data.get("data")[0].get("images").get("original").get("url")
    print(data)

    context = {
        'person' : person,
        'image' : image
    }

    return render(request, 'jobs/past_life.html', context)