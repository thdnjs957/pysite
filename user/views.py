from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def joinform(request):
    return render(request, 'user/joinform.html')

def join(request):
    user = User()
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()

    return HttpResponseRedirect('/user/joinsuccess')  # 함수 만들어서 거기서 html 보이게

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    results = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])  # 필터 걸어서 객체를 뺴낸다
    print(results)
    # 로그인 실패
    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 처리
    authuser = results[0]  # 객체가 왜 리스트로 나옴??
    request.session['authuser'] = model_to_dict(authuser)  # session 객체에 authuser 넣기 # 객체를 dict 형태로 converting

    return HttpResponseRedirect('/')

def logout(request):
    del request.session['authuser']  # session에 저장된 놈 날 려 ~^~ 배고프당
    return HttpResponseRedirect('/')

def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])  # 쿼리가 들어간거임 db에서 가져옴 dictionary 이니깐
    data = {
        'user': user
    }
    return render(request, 'user/updateform.html', data)


def update(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']

    user.gender = request.POST['gender']

    if request.POST['password'] is not '':
        user.password = request.POST['password']

    user.save()  # 비어있으면 insert 아니면 update 친다

    # SESSION_SAVE_EVERY_REQUEST = True 추가
    # request.session['authuser'] = model_to_dict(user)
    request.session['authuser']['name'] = user.name
    return HttpResponseRedirect('/user/updateform?result=success')


def checkemail(request):

    # email = request.GET['email']
    try:
        user = User.objects.get(email=request.GET['email'])
    except Exception as e:
        user = None

    result = {
        'result': 'success',
        'data': "not exist" if user is None else "exist"
        # model_to_dict(user)
    }

    return JsonResponse(result)