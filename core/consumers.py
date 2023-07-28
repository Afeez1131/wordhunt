import datetime
import json
import threading
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from django.template.loader import render_to_string


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

    def connect(self):
        print('connecting to lobby chat...')
        args = self.scope.get('url_route').get('kwargs').get('name')
        print('args: ', args)
        self.accept()

    def disconnect(self, code):
        return super(LobbyChatConsumer, self).disconnect(code)

    def receive_json(self, content, **kwargs):
        print('content: ', content)
