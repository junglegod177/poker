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
            self.table_group_name,
            self.channel_name
        )

        self.accept()

        player = Player.objects.create(username=self.user.username)
        table = Table.objects.get(name = table_name)
        player.join_table(table)


        #tip vodi na funkciju, slicno ka view u url
        """
        async_to_sync(self.channel_layer.group_send)(
            self.table_group_name, {"type": "test", "message": 'kurac'}
        )
        """

    def disconnect(self, close_code):
        table_name = self.scope['url_route']['kwargs']['table_name']
        table = Table.objects.get(name = table_name)
        player = Player.objects.get(username=self.user.username)
        player.delete()
        table.save()

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')


    """
    def test(self, event):
        message = event['message']
        print("Test message received:", message)
        self.send(text_data=json.dumps({
            "poruka": 'kurac'
        }))
    """