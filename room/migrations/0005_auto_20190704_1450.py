# Generated by Django 2.2.2 on 2019-07-04 14:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('room', '0004_auto_20190704_0737'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoomSchedule',
            new_name='RoomRequest',
        ),
    ]
