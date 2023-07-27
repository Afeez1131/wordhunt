from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class WordHuntConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(WordHuntConsumer, self).__init__(*args, **kwargs)
        self.room_name = 'game_room'

    def connect(self):
        print('-----------connecting---------------')
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def disconnect(self, code):
        print('----------disconnecting------------')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, content, **kwargs):
        print('-----------incoming json content from client----------')
        print(content)


