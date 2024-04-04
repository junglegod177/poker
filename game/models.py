from django.db import models
from django.contrib import admin
import json, random

# Create your models here.

class Player(models.Model):
    username = models.CharField(max_length=50)
    chips = models.IntegerField(default=10000)
    hand = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def join_table(self, table):
        occupied_seats = Seat.objects.filter(table=table).order_by('seat_number')
        for i in range(1, 9):
            if not occupied_seats or occupied_seats[0].seat_number > i:
                break
            occupied_seats = occupied_seats[1:]
        else:
            raise Exception('Table is full')

        Seat.objects.create(table=table, player=self, seat_number=i)

        table.players_number += 1
        table.save()

        return i

    def leave_table(self, table):
        Seat.objects.get(table=table, player=self).delete()

        self.delete()

        table.players_number -= 1
        table.save()


class Table(models.Model):
    name = models.CharField(max_length=50)
    blinds = models.CharField(max_length=15)
    players_number = models.IntegerField(default=0)
    deck = models.CharField(max_length=1000, blank=True, null=True)
    dealer = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
    def can_start_game(self):
        return True if self.players_number > 1 else False
    
    def start(self):
        self.deck = self.create_deck()
        self.deal_cards()
        self.pay_blinds()

    def create_deck(self):
        ranks = range(2, 15)
        suits = range(4)
        deck = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return json.dumps(deck)  # Convert the deck to a string

    def deal_cards(self):
        deck = json.loads(self.deck)  # Convert the deck back to a list
        seats = Seat.objects.filter(table=self)
        for seat in seats:
            seat.player.hand = json.dumps([deck.pop(), deck.pop()])
            seat.player.save()
        self.deck = json.dumps(deck)
        self.save()

    def pay_blinds(self):
        small_blind, big_blind = self.blinds.split('/')
        dealer_seat = Seat.objects.get(table=self, seat_number=self.dealer)

        if self.players_number == 2:
            dealer_player = dealer_seat.player
            dealer_player.chips -= int(big_blind)

            # Get the other player
            next_seat_number = self.get_next_occupied_seat(self.dealer)
            small_blind_seat = Seat.objects.get(table=self, seat_number=next_seat_number)
            
            small_blind_player = small_blind_seat.player
            small_blind_player.chips -= int(small_blind)

        else:
            pass

    def get_next_occupied_seat(self, current_seat):
        next_seat_number = current_seat + 1

        while True:
            next_seat = Seat.objects.get(table=self, seat_number=next_seat_number)
            if next_seat.player is not None:
                return next_seat_number

            next_seat_number = (next_seat_number % self.players.count()) + 1

    def get_table_state(self):
        seats = Seat.objects.filter(table=self).order_by('seat_number')
        state = [
            {
                "position": seat.seat_number,
                "username": seat.player.username,
                "chips": seat.player.chips,
                "playersNumber": seat.table.players_number
            }
            for seat in seats
        ]

        return state
    
class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    seat_number = models.IntegerField()

    def __str__(self):
        return f"Seats for {self.table.name}"

class CommunityCards(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cards = models.CharField(max_length=15)

    def __str__(self):
        return f"Community cards for {self.table.name}"
    
class Card:
    RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SUITS = {
        0 : "H",
        1 : "S",
        2 : "D",
        3 : "C"
    }

    def __init__(self, rank, suit):
        if rank not in self.RANKS or suit not in self.SUITS:
            raise ValueError("Invalid card rank or suit")
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"



admin.site.register(Table)
admin.site.register(Player)

# Assuming you have a Table instance called "table_instance"
# You can add players to the table like this:
"""
table_instance.players.add(player1, player2, player3)
"""

# You can also remove players from the table:
"""
table_instance.players.remove(player1)
"""

# Get all players associated with a table:
"""
players_on_table = table_instance.players.all()
"""