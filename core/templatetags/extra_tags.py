from django import template

from core.models import Lobby

register = template.Library()


@register.simple_tag
def is_game_creator(request, uuid):
    if Lobby.objects.filter(lobby_name=uuid).exists():
        lobby = Lobby.objects.get(lobby_name=uuid)
        if lobby.game_room.creator == request.user:
            return True
        return False
    return False
