# Generated by Django 4.2.3 on 2023-07-28 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameroom',
            name='room_name',
            field=models.UUIDField(default='43909555d753410892bab308e34d01d0', unique=True),
        ),
    ]