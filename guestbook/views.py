from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    guestbook = Guestbook.objects.all().order_by('-id')
    data = {'guestbooklist': guestbook}

    return render(request, 'guestbook/list.html', data)

def add(request):

    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['content']
    guestbook.save()
    return HttpResponseRedirect('/guestbook')

def deleteform(request, id = 0):
    data = {'id': id}
    return render(request, 'guestbook/deleteform.html', data)

def delete(request):
    get_id = request.POST['id']
    get_password = request.POST['password']
    guestbook = Guestbook.objects.filter(id=get_id).filter(password=get_password)
    guestbook.delete()
    return HttpResponseRedirect('/guestbook')


