import json, re
from .models import Table, Player, Seat
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
        seat_position = player.join_table(table)

        table_state = table.get_table_state()

        async_to_sync(self.channel_layer.group_send)(
            self.table_group_name,
            {
                "type": "player_join",
                "position": seat_position,
                "username": player.username
            }
        )

        self.send(text_data=json.dumps({
            "action": "table_state",
            "state": table_state
        }))

        if table.can_start_game():
            self.start_game(table)

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
        player.leave_table(table)
        table.save()

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

    def player_join(self, event):
        self.send(text_data=json.dumps({
            "action": "player_join",
            "position": event['position'],
            "username": event['username']
        }))

    def start_game(self, table):
        table.start()

        async_to_sync(self.channel_layer.group_send)(
            self.table_group_name,
            {
                "type": "game_started",
            }
        )

    def game_started(self, event):

        table_name = self.scope['url_route']['kwargs']['table_name']
        table = Table.objects.get(name=table_name)
        seats = Seat.objects.filter(table=table)
        for seat in seats:
            self.send(text_data=json.dumps({
                "action": "deal_cards",
                "seat_position": seat.seat_number,
                "cards": json.loads(seat.player.hand)
            }))


    """
    def test(self, event):
        message = event['message']
        print("Test message received:", message)
        self.send(text_data=json.dumps({
            "poruka": 'kurac'
        }))
    """