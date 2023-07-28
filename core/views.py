from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'core/index.html', {})

@login_required
def lobby(request):
    return render(request, 'core/lobby.html', {})


def chatroom(request):
    return render(request, 'core/chatroom.html')


def login(request):
    return render(request, 'core/login.html')
