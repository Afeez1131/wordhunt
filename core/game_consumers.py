import datetime
import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string

from core.models import GameRoom

logger = logging.getLogger(__name__)


class GameRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(GameRoomConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.user = None

    def connect(self):
        logger.info('connecting to the game room')
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            logger.info('closing connection, user not authenticated')
            self.close()
        room_name = self.scope.get('url_route').get('kwargs').get('room_uuid')
        self.room_name = str(room_name)
        if not GameRoom.objects.filter(room_name=self.room_name).exists():
            logger.info(f'invalid room name {self.room_name}')
            self.close()
        logger.info('accepting connection')
        self.accept()
        logger.info(f'adding user to {self.room_name}')

        self.send_json({
            'message': f'connection successful {self.user.username}'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def close(self, code=None):
        logger.info('closing connection')
        return super(GameRoomConsumer, self).close(code)

    def disconnect(self, code=None):
        logger.info(f'disconnecting from {self.room_name}')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, content, **kwargs):
        logger.info('incoming content from client: ')
        action = content.get('action')
        data = content.get('data')
        if action == 'player_message':
            message = data.get('message')
            context = {'message': message,
                       'time': str(datetime.datetime.now().strftime("%H:%M:%S")),
                       'username': self.user.username}
            sender_template = render_to_string('core/message_sender.html', context)
            receiver_template = render_to_string('core/message_receiver.html', context)
            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'echo_user_response',
                'data': {
                    'sender_template': sender_template,
                    'receiver_template': receiver_template,
                    'sender': data.get('sender')
                }
            })

    def echo_user_response(self, event):
        self.send_json(event)

    def game_rule(self, event):
        self.send_json(event)


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
