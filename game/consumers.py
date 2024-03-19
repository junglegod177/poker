import json
from .models import Table
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TablePlayer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.accept()

        self.table_group_name = "table_%s" % self.user
        print(self.table_group_name)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'sit':
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            if table.players_number < 7:
                table.players_number += 1
                table.save()
                self.send(text_data=json.dumps({
                    'type': 'sit',
                    'message': table.players_number,                
                }))

        elif action == 'unsit':
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            table.players_number -= 1
            table.save()
            self.send(text_data=json.dumps({
                'message': table.players_number,                
            }))
