import asyncio
import datetime
import json
import logging
import threading
import time

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string

from core.models import GameRoom
from core.utils import send_api_request

logger = logging.getLogger(__name__)


class GameRoomConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(GameRoomConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.user = None

    async def connect(self):
        logger.info('connecting to the game room')
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            logger.info('closing connection, user not authenticated')
            await self.close()
            return

        room_name = self.scope.get('url_route').get('kwargs').get('room_uuid')
        self.room_name = str(room_name)
        if not await database_sync_to_async(GameRoom.objects.filter(room_name=self.room_name).exists)():
            logger.info(f'invalid room name {self.room_name}')
            await self.close()
            return
        logger.info('accepting connection into the game room')
        await self.accept()
        logger.info(f'connection accepted: adding {self.user.username} to {self.room_name}')

        await self.send_json({
            'message': f'connection successful {self.user.username}'
        })
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.game_countdown(10)

    async def close(self, code=None):
        logger.info('closing connection')
        return super(GameRoomConsumer, self).close(code)

    async def disconnect(self, code=None):
        logger.info('disconnecting user...')
        if self.user.is_authenticated:
            logger.info(f'disconnecting {self.user} from {self.room_name}')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        logger.info('incoming content from client: ')
        logger.info('content: ', content)
        action = content.get('action')
        data = content.get('data')
        if action == 'player_message':
            message = data.get('message')
            context = {'message': message,
                       'time': str(datetime.datetime.now().strftime("%H:%M:%S")),
                       'username': self.user.username}
            sender_template = await database_sync_to_async(render_to_string)('core/message_sender.html', context)
            receiver_template = await database_sync_to_async(render_to_string)('core/message_receiver.html', context)
            await self.channel_layer.group_send(self.room_name, {
                'type': 'echo_user_response',
                'data': {
                    'sender_template': sender_template,
                    'receiver_template': receiver_template,
                    'sender': data.get('sender')
                }
            })

    async def game_countdown(self, countdown):
        while countdown > 0:
            message = await database_sync_to_async(render_to_string)('core/countdown.html', {'countdown': countdown})

            await self.send_json({
                'type': 'countdown',
                'countdown': message
            })
            countdown -= 1
            await asyncio.sleep(2)

    # async def verify_word(self):
    #     valid_english = await send_api_request(countdown)
    def countdown(self, event):
        self.send_json(event)

    async def echo_user_response(self, event):
        await self.send_json(event)

    async def game_rule(self, event):
        await self.send_json(event)

    async def send_base_word(self, event):
        await  self.send_json(event)


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
