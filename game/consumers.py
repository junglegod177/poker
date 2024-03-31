import json, re
from .models import Table, Player
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class TablePlayer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']

        table_name = self.scope['url_route']['kwargs']['table_name']
        sanitized_table_name = re.sub(r'\W+', '_', table_name)
        self.table_group_name = f"table_{sanitized_table_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.table_group_name, self.channel_name
        )
        self.accept()

        #tip vodi na funkciju, slicno ka view u url
        """
        async_to_sync(self.channel_layer.group_send)(
            self.table_group_name, {"type": "test", "message": 'kurac'}
        )
        """

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        #nekad probat u connect
        if action == 'sit':
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            if table.players_number < 8:
                table.players_number += 1
                player = Player.objects.create(username=self.user.username)
                table.players.add(player)
                table.save()
                self.send(text_data=json.dumps({
                    'type': 'sit',
                    'message': table.players_number,                
                }))

        #nekad probat u disconnect
        elif action == 'unsit':
            table_name = data.get('table_name')
            table = Table.objects.get(name = table_name)
            table.players_number -= 1
            player = Player.objects.get(username=self.user.username)
            player.delete()
            #then table players remove is not needed right?
            table.save()

    """
    def test(self, event):
        message = event['message']
        print("Test message received:", message)
        self.send(text_data=json.dumps({
            "poruka": 'kurac'
        }))
    """