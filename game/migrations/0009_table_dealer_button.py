# Generated by Django 5.0.3 on 2024-04-04 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_player_hand'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='dealer_button',
            field=models.IntegerField(default=1),
        ),
    ]
