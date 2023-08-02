from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.decorators import forbidden_view
from core.models import Lobby, GameRoom
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
    game_lobby = Lobby.objects.get(lobby_name=lobby_name)
    return render(request, 'core/lobby.html', {'lobby': game_lobby})


def verify_code(request):
    code = request.POST.get('code')
    if Lobby.objects.filter(shortcode=code).exists():
        lobby = Lobby.objects.get(shortcode=code)
        return HttpResponseRedirect(reverse('core:lobby', args=[lobby.lobby_name]))
    messages.error(request, 'Invalid Code')
    logger.info('invalid code')
    return HttpResponseRedirect(reverse('accounts:login'))


def chatroom(request, room_name):
    if not GameRoom.objects.filter(room_name=room_name).exists():
        messages.error(request, 'Invalid Room Name')
        return HttpResponseRedirect(reverse('accounts:login'))
    game_room = GameRoom.objects.get(room_name=room_name)
    return render(request, 'core/chatroom.html', {'game_room': game_room})


def login(request):
    return render(request, 'core/login.html')
