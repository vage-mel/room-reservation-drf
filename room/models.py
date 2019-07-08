from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=128, null=True, blank=True)
    chair_count = models.IntegerField(default=0)
    is_projector = models.BooleanField(default=False)
    is_board = models.BooleanField(default=False)


class Status(models.Model):
    created = 1
    confirmed = 2
    rejected = 3

    name = models.CharField(max_length=32)


class RoomRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='early_reservation_time', on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=Status.objects.get(id=Status.created))


