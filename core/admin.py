from django.contrib import admin

from core.models import GameRoom, Lobby


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'members_count']
    list_filter = ['room_name']


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ['game_room', 'lobby_name', 'joined_count']
    list_filter = ['game_room', 'lobby_name']
