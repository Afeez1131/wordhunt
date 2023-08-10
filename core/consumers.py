import datetime
import json
import threading
import time

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
import logging
from channels.exceptions import StopConsumer
from django.urls import reverse

from core.models import Lobby, GameRoom

logger = logging.getLogger(__name__)


class LobbyChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(LobbyChatConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.lobby = None
        self.user = None

    async def connect(self):
        logger.info('connecting to lobby chat...')
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            logger.info('user not authenticated')
            await self.close(code='103')
            return
        lobby_uuid = self.scope.get('url_route').get('kwargs').get('uuid')
        if not await database_sync_to_async(Lobby.objects.filter(lobby_name=lobby_uuid).exists)():
            logger.info(f'invalid lobby uuid: {lobby_uuid}')
            await self.close()
            await self.disconnect()
            return
        else:
            self.lobby = await database_sync_to_async(Lobby.objects.get)(lobby_name=lobby_uuid)
            lobby_name = str(self.lobby.lobby_name)
            self.room_name = lobby_name
            await self.accept()
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.send_join_alert()
            await database_sync_to_async(self.lobby.add)(self.user.id)
            members_count = await database_sync_to_async(self.lobby.members.count)()
            if members_count > 1:
                await self.send_all_members()
            else:
                await self.send_player_information()
            members = await self.get_lobby_member()
            logger.info(f'websocket connection established for {self.user} in {self.room_name}')

    async def close(self, code=None):
        logger.info('closing connection...')
        return super(LobbyChatConsumer, self).close(code)

    async def disconnect(self, code=None):
        logger.info('disconnecting...')
        logger.info(f'{self.user} disconnected from {self.room_name}')
        if self.user.is_authenticated:
            await self.send_left_alert()
            await self.send_all_members()
            await database_sync_to_async(self.lobby.remove)(self.user.id)
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        return super(LobbyChatConsumer, self).disconnect(code)

    async def receive_json(self, content, **kwargs):
        print('content received...', )
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
            message_sender = await database_sync_to_async(render_to_string)('core/message_sender.html', context)
            message_receiver = await database_sync_to_async(render_to_string)('core/message_receiver.html', context)

            await self.channel_layer.group_send(self.room_name, {
                'type': 'echo_message',
                'data': {
                    'message_sender': message_sender,
                    'message_receiver': message_receiver,
                    'sender': sender
                }
            })
        if action == 'start_game':
            rn = await database_sync_to_async(GameRoom.objects.get)(lobby=self.lobby)
            room_name = str(rn.room_name)
            url = await self.create_game_room_url(room_name)
            await self.channel_layer.group_send(self.room_name, {
                'type': 'start_game',
                'data': {
                    'game_room': url
                }
            })

    async def get_lobby_member(self):
        members = await database_sync_to_async(self._get_members)()
        return members

    def _get_members(self):
        members = list(self.lobby.members.all())
        return members

    async def send_join_alert(self):
        msg = '{} join the lobby'.format(self.user.username)
        message = await database_sync_to_async(render_to_string)('core/alert.html', {'message': msg})
        await self.channel_layer.group_send(self.room_name, {
            'type': 'join_chat_alert',
            'data': {
                'message': message,
                'player': self.user.username
            }
        })

    async def send_left_alert(self):
        msg = '{} exit the lobby'.format(self.user.username)
        message = await database_sync_to_async(render_to_string)('core/alert.html', {'message': msg})
        await self.channel_layer.group_send(self.room_name, {
            'type': 'left_chat_alert',
            'data': {
                'message': message,
                'player': self.user.username
            }
        })

    async def send_player_information(self):
        player = self.user.username
        player_image = await database_sync_to_async(render_to_string)('core/player_image.html', {'username': player})
        await self.channel_layer.group_send(self.room_name,
                                            {
                                                'type': 'player_joined',
                                                'data': {
                                                    'message': '{} joined the Lobby'.format(player),
                                                    'image': player_image,
                                                    'joined_user': player
                                                }
                                            })

    async def send_all_members(self):
        players = await database_sync_to_async(self.lobby.members.all)()
        players_images = await database_sync_to_async(render_to_string)(
            'core/all_players_image.html',
            {'players': players}
        )
        await self.channel_layer.group_send(self.room_name, {
            'type': 'all_players',
            'data': {
                'images': players_images,

            }
        })

    async def create_game_room_url(self, game_room_name):
        url = reverse(
            'core:game_room',
            args=[game_room_name]
        )
        print('url: ', url)
        return url

    async def player_joined(self, event):
        await self.send_json(event)

    async def all_players(self, event):
        await self.send_json(event)

    async def echo_message(self, event):
        await self.send_json(event)

    async def join_chat_alert(self, event):
        await self.send_json(event)

    async def left_chat_alert(self, event):
        await self.send_json(event)

    async def start_game(self, event):
        await self.send_json(event)
