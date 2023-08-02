import datetime
import json
import threading
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
import logging

from django.urls import reverse

from core.models import Lobby, GameRoom

logger = logging.getLogger(__name__)

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
        self.send_join_alert()
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
        self.send_left_alert()
        logger.info(f'removing {self.user} from {self.room_name}')
        self.lobby.remove(self.user.id)
        self.send_all_members()
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        # return super(LobbyChatConsumer, self).disconnect(code)

    def receive_json(self, content, **kwargs):
        print('content receiver...', content)
        action = content.get('action')
        data = content.get('data')
        if action == 'new_message':
            message = data.get('message')
            sender = data.get('sender')
            context = {
                'message': message,
                'time': str(datetime.datetime.now().strftime("%H: %M: %S")),
                'username': sender
            }
            message_sender = render_to_string('core/message_sender.html', context)
            message_receiver = render_to_string('core/message_receiver.html', context)

            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'echo_message',
                'data': {
                    'message_sender': message_sender,
                    'message_receiver': message_receiver,
                    'sender': sender
                }
            })
        if action == 'start_game':
            url = reverse('core:game_room', args=[self.lobby.game_room.room_name])
            logger.info('Game ROOM URL: ', url)
            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'start_game',
                'data': {
                    'game_room': url
                }
            })

    def send_join_alert(self):
        msg = '{} join the lobby'.format(self.user.username)
        message = render_to_string('core/alert.html', {'message': msg})
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'join_chat_alert',
            'data': {
                'message': message,
                'player': self.user.username
            }
        })

    def send_left_alert(self):
        msg = '{} exit the lobby'.format(self.user.username)
        message = render_to_string('core/alert.html', {'message': msg})
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'left_chat_alert',
            'data': {
                'message': message,
                'player': self.user.username
            }
        })

    def send_player_information(self):
        player = self.user.username
        player_image = render_to_string('core/player_image.html', {'username': player})
        async_to_sync(self.channel_layer.group_send)(self.room_name,
                                                     {
                                                         'type': 'player_joined',
                                                         'data': {
                                                             'message': '{} joined the Lobby'.format(player),
                                                             'image': player_image,
                                                             'joined_user': player
                                                         }
                                                     })

    def send_all_members(self):
        players = self.lobby.members.all()
        logger.info(players)
        players_images = render_to_string('core/all_players_image.html', {'players': players})
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'all_players',
            'data': {
                'images': players_images,

            }
        })

    def player_joined(self, event):
        self.send_json(event)

    def all_players(self, event):
        self.send_json(event)

    def echo_message(self, event):
        self.send_json(event)

    def join_chat_alert(self, event):
        self.send_json(event)

    def left_chat_alert(self, event):
        self.send_json(event)

    def start_game(self, event):
        self.send_json(event)
