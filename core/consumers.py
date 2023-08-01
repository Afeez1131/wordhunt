import datetime
import json
import threading
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
import logging

from core.models import Lobby

logger = logging.getLogger(__name__)


class WordHuntConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(WordHuntConsumer, self).__init__(*args, **kwargs)
        self.room_name = 'game_room'

    def connect(self):
        print('-----------connecting---------------')
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send_json({
            'action': 'connected',
            'message': 'You are connected to the webscoket',
            'html': render_to_string('core/login.html'),
            'selector': '#container'
        })

    def disconnect(self, code):
        print('----------disconnecting------------')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, content, **kwargs):
        print('-----------incoming json content from client----------')
        print(content, type(content))
        action = content.get('action')
        data = content.get('data')
        print('data: ', json.loads(data))
        if action == 'authenticate':
            request = data.get('request')
            username = data.get('username')
            password = data.get('password')
            print(request, username, password)
            # user = authenticate(request, username=username, password=password)


"""
    "Let's kick off with the word 'delightful'!"
    "Your challenge begins with the word 'magnificent'!"
    "Get ready to create words from 'fascinating'!"
    "Today's base word is 'adventure.' Let the game begin!"
    "Form new words from the base word 'wonderful'!"
    "The starting word is 'breathtaking.' Good luck, WordWarriors!"
    "We'll start with the word 'fantastic.' Happy word-building!"
"""

"""
    "Time for a new challenge! The word now is 'spectacular'!"
    "Let's level up! Your next base word is 'unbelievable'!"
    "Get ready for the next word: 'extraordinary'!"
    "Here comes the next base word: 'marvelous'!"
    "On to the next one! The word is now 'phenomenal'!"
    "New word alert: 'astonishing'! Keep those words coming!"
    "Ready for more? Your next word is 'remarkable'!"
"""

"""
    "Congratulations to our WordWarrior champion! The winner is [Player's Name]!"
    "And the crown of WordWarrior goes to [Player's Name] for their outstanding word skills!"
    "Give it up for our victorious WordWarrior, [Player's Name]!"
    "A round of applause for the winner of this word battle, [Player's Name]!"
    "We have a winner, and it's none other than [Player's Name]! Well done!"
    "The word master who emerged victorious is [Player's Name]! Incredible job!"
    "And the title of WordWarrior for this game goes to [Player's Name]! Well-deserved!"
"""


class LobbyChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(LobbyChatConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.lobby = None
        self.user = None

    def connect(self):
        logger.info('connecting to lobby chat...')
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            logger.info('user not authenticated')
            self.close(code='103')
        lobby_uuid = self.scope.get('url_route').get('kwargs').get('uuid')
        if not Lobby.objects.filter(lobby_name=lobby_uuid).exists():
            logger.info(f'invalid lobby uuid: {lobby_uuid}')
            self.close()
        self.accept()
        self.lobby = Lobby.objects.get(lobby_name=lobby_uuid)
        self.room_name = str(self.lobby.lobby_name)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.lobby.add(self.user.id)
        if self.lobby.members_count > 1:
            self.send_all_members()
        else:
            self.send_player_information()
        logger.info(f'websocket connection established for {self.user} in {self.room_name}')

    def close(self, code=None):
        logger.info('closing connection...')
        return super(LobbyChatConsumer, self).close(code)

    def disconnect(self, code=None):
        logger.info('disconnecting...')
        logger.info(f'removing {self.user} from {self.room_name}')
        self.lobby.remove(self.user.id)
        self.send_all_members()
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        # return super(LobbyChatConsumer, self).disconnect(code)

    def receive_json(self, content, **kwargs):
        print('content: ', content)

    def send_player_information(self):
        player = self.user.username
        player_image = render_to_string('core/player_image.html', {'username': player})
        async_to_sync(self.channel_layer.group_send)(self.room_name,
                                                     {
                                                         'type': 'player_joined',
                                                         'data': {
                                                             'message': '{} joined the Lobby'.format(player),
                                                             'image': player_image
                                                         }
                                                     })

    def send_all_members(self):
        players = self.lobby.members.all()
        logger.info(players)
        players_images = render_to_string('core/all_players_image.html', {'players': players})
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'all_players',
            'data': {
                'images': players_images
            }
        })
    def player_joined(self, event):
        self.send_json(event)

    def all_players(self,event):
        self.send_json(event)
