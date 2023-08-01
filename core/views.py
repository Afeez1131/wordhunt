from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.decorators import forbidden_view
from core.models import Lobby
import logging

logger = logging.getLogger('core')

# Create your views here.

def index(request):
    logger.info('on the index page')
    return render(request, 'core/index.html', {})

def lobby(request, lobby_name):
    if not Lobby.objects.filter(lobby_name=lobby_name).exists():
        logger.info('invalid lobby name')
        messages.error(request, 'Invalid Lobby Name')
        return HttpResponseRedirect(reverse('accounts:login'))
    return render(request, 'core/lobby.html', {})


def verify_code(request):
    code = request.POST.get('code')
    if Lobby.objects.filter(shortcode=code).exists():
        lobby = Lobby.objects.get(shortcode=code)
        return HttpResponseRedirect(reverse('core:lobby', args=[lobby.lobby_name]))
    messages.error(request, 'Invalid Code')
    logger.info('invalid code')
    return HttpResponseRedirect(reverse('accounts:login'))


def chatroom(request):
    return render(request, 'core/chatroom.html')


def login(request):
    return render(request, 'core/login.html')
