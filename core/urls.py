from django.urls import path

from core import views
from core.ajax import ajax_create_game

app_name = 'core'
urlpatterns = [
    path('', views.index, name='home'),
    path('verify-code', views.verify_code, name='verify_code'),
    path('start-game', ajax_create_game, name='ajax_create_game'),
    path('lobby/<uuid:lobby_name>', views.lobby, name='lobby'),
    path('chat', views.chatroom, name='chat'),
]
