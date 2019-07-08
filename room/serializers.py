import time

from rest_framework import serializers

from auths.serializers import UserSerializer
from .models import Room, RoomRequest, Status


class RoomSerializer(serializers.ModelSerializer):
    early_reservation_time = serializers.SerializerMethodField(source='get_early_reservation_time', read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'chair_count', 'is_projector', 'is_board', 'early_reservation_time')
        read_only_fields = ('id', )

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.chair_count = validated_data.get('chair_count', instance.chair_count)
        instance.is_projector = validated_data.get('is_projector', instance.is_projector)
        instance.is_board = validated_data.get('is_board', instance.is_board)
        instance.save()

        return instance

    def get_early_reservation_time(self, room):
        qs = RoomRequest.objects.filter(room=room,
                                        start_date_time__gte=time.strftime("%Y-%m-%d"),
                                        status=Status.confirmed).order_by('start_date_time').first()
        serializer = EarlyReservationTimeSerializer(instance=qs)
        return serializer.data


class EarlyReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRequest
        fields = ('start_date_time', 'end_date_time')


class StatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Status
        fields = ('id', 'name')


class RoomRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = RoomRequest
        fields = ('id', 'user', 'room', 'start_date_time', 'end_date_time')
        read_only_fields = ('id',)

    def validate(self, data):

        if data.get('start_date_time') and data['start_date_time'] > data['end_date_time']:
            raise serializers.ValidationError("Введите дату и время начала меньше чем дату и время окончания.")

        return data

    def create(self, validated_data):
        return RoomRequest.objects.create(**validated_data)


class RoomRequestFullSerializer(RoomRequestSerializer):
    status = StatusSerializer()

    class Meta(RoomRequestSerializer.Meta):
        fields = RoomRequestSerializer.Meta.fields + ('status',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        room_schedule = super().create(validated_data)
        return room_schedule

    def update(self, instance, validated_data):
        status = validated_data.pop('status')

        if status:
            instance.status_id = status.get('id')

        instance.save()

        return instance
