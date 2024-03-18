from django.db import models
from django.contrib import admin

# Create your models here.

class Table(models.Model):
    name = models.CharField(max_length=50)
    blinds = models.CharField(max_length=15)
    players_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Player(models.Model):
    username = models.CharField(max_length=50)
    chips = models.IntegerField()
    cards = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.username

class TableInfo(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class CommunityCards(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cards = models.CharField(max_length=15)

    def __str__(self):
        return f"Community cards for {self.table.name}"


admin.site.register(Table)
admin.site.register(Player)
admin.site.register(TableInfo)