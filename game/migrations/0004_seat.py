# Generated by Django 5.0.3 on 2024-04-03 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_table_players_alter_player_chips_delete_tableinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.player')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.table')),
            ],
        ),
    ]
