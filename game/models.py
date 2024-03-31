from django.db import models
from django.contrib import admin

# Create your models here.

class Player(models.Model):
    username = models.CharField(max_length=50)
    chips = models.IntegerField(default=10000)
    cards = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.username

class Table(models.Model):
    name = models.CharField(max_length=50)
    blinds = models.CharField(max_length=15)
    players_number = models.IntegerField(default=0)
    players = models.ManyToManyField(Player, related_name='tables', blank=True)

    def __str__(self):
        return self.name

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