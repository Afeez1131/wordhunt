from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lobby', views.lobby, name='lobby'),
    path('chat', views.chatroom, name='chat'),
]
