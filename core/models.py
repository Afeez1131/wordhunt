import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class GameRoom(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4, unique=True)
    members = models.ManyToManyField(User, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_rooms', null=True, blank=True)
    members_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {} members'.format(self.room_name, self.members_count)

    class Meta:
        ordering = ('-id',)
        get_latest_by = 'id'


class Lobby(models.Model):
    game_room = models.OneToOneField(GameRoom, on_delete=models.CASCADE)
    lobby_name = models.UUIDField(default=uuid.uuid4, unique=True)
    shortcode = models.CharField(max_length=33, blank=True, null=True)
    members = models.ManyToManyField(User, blank=True)
    joined_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}'.format(self.game_room.room_name, self.joined_count)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.shortcode:
            shortcode = str(self.lobby_name).split('-')[0]
            while Lobby.objects.filter(shortcode=shortcode).exists():
                shortcode = str(uuid.uuid4()).split('-')[0]
            self.shortcode = shortcode
        return super(Lobby, self).save()
