import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class GameRoom(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4().hex, unique=True)
    members = models.ManyToManyField(User, blank=True)
    members_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}: {} members'.format(self.room_name, self.members_count)

    class Meta:
        ordering = ('-id',)


class Lobby(models.Model):
    game_room = models.OneToOneField(GameRoom, on_delete=models.CASCADE)
    lobby_name = models.UUIDField(default=uuid.uuid4(), unique=True)
    members = models.ManyToManyField(User, blank=True)
    joined_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return '{}: {}'.format(self.game_room.room_name, self.joined_count)
