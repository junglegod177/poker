from django.db import models
from django.contrib import admin

# Create your models here.

class Player(models.Model):
    username = models.CharField(max_length=50)
    chips = models.IntegerField(default=10000)
    cards = models.CharField(max_length=5, blank=True, null=True)

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

        # Create a new Seat instance
        Seat.objects.create(table=table, player=self, seat_number=i)

        table.players_number += 1
        table.save()

        return i

    def leave_table(self, table):
        Seat.objects.get(table=table, player=self).delete()

        self.delete()

        table.players_number -= 1
        print("AAAAAA")
        table.save()


class Table(models.Model):
    name = models.CharField(max_length=50)
    blinds = models.CharField(max_length=15)
    players_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def get_table_state(self):
        seats = Seat.objects.filter(table=self).order_by('seat_number')
        state = [
            {
                "position": seat.seat_number,
                "username": seat.player.username,
                "chips": seat.player.chips
            }
            for seat in seats
        ]

        return state
    
class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    seat_number = models.IntegerField()

    def __str__(self):
        return f"Community cards for {self.table.name}"

class CommunityCards(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cards = models.CharField(max_length=15)

    def __str__(self):
        return f"Community cards for {self.table.name}"


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