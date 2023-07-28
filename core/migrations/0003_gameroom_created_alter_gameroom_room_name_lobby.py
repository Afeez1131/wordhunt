# Generated by Django 4.2.3 on 2023-07-28 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_gameroom_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameroom',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameroom',
            name='room_name',
            field=models.UUIDField(default='4cc5993fb58f4d8f8e69a6d3a775c145', unique=True),
        ),
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby_name', models.UUIDField(default=uuid.UUID('06bd8ac0-e712-45b1-8d34-44e6b0eecd93'), unique=True)),
                ('joined_count', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('game_room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.gameroom')),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
