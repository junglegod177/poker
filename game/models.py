from django.db import models
from django.contrib import admin

# Create your models here.

class Table(models.Model):
    name = models.CharField(max_length=50)
    blinds = models.CharField(max_length=15)
    players = models.IntegerField(default=0)

    def __str__(self):
        return self.name


admin.site.register(Table)