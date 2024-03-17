import json
from .models import Table
from django.http import JsonResponse

from channels.generic.websocket import WebsocketConsumer


class TablePlayer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def disconnect(self, close_code):
        print("EEEEEEEEEEEEEEEEEEEEE")
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'sit':
            print("AAAAAAAAAAAAA")
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            if table.players < 7:
                table.players += 1
                table.save()
                self.send(text_data=json.dumps({
                    'message': table.players,                
                }))

        elif action == 'unsit':
            print("EEEEEEEEE")
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            table.players -= 1
            table.save()
            self.send(text_data=json.dumps({
                'message': table.players,                
            }))
