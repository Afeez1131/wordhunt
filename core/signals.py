from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import GameRoom, Lobby


@receiver(post_save, sender=GameRoom)
def update_members_count(sender, instance, created, **kwargs):
    if created:
        Lobby.objects.create(game_room=instance)
    count = instance.members.count()
    instance.members_count = count
    instance.save()


@receiver(post_save, sender=Lobby)
def update_user_joined_lobby(sender, instance, **kwargs):
    instance.joined_count = instance.members.count()
    instance.save()
