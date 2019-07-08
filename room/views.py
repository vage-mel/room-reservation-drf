from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from .models import Room, RoomRequest, Status
from .serializers import RoomSerializer, RoomRequestSerializer, RoomRequestFullSerializer
from .permissions import IsStaffOrReadOnly, IsOwnerOrIsStaffOrReadOnly


class RoomList(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsStaffOrReadOnly
    )

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsStaffOrReadOnly
    )

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room)

        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChoiceRoomRequestSerializerMixin:
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return RoomRequestFullSerializer
        return RoomRequestSerializer


class RoomRequestList(APIView, ChoiceRoomRequestSerializerMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, room_id=None):
        rooms_requests = RoomRequest.objects.all().order_by('start_date_time', 'end_date_time')

        if request.GET.get('status') and hasattr(Status, request.GET.get('status')):
            rooms_requests = rooms_requests.filter(status__id=getattr(Status, request.GET.get('status')))

        if room_id:
            rooms_requests = rooms_requests.filter(room__id=room_id)

        serializer = self.get_serializer_class()(rooms_requests, many=True)

        return Response(serializer.data)

    def post(self, request, room_id):
        serializer = self.get_serializer_class()(data=request.data, partial=True)

        if serializer.is_valid():

            if room_id:
                serializer.save(user=self.request.user, room=Room.objects.get(pk=room_id))
            else:
                serializer.save(user=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomRequestDetail(APIView, ChoiceRoomRequestSerializerMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrIsStaffOrReadOnly
    )

    def get_object(self, pk):
        try:
            room_request = RoomRequest.objects.get(pk=pk)
            self.check_object_permissions(self.request, room_request)
            return room_request
        except RoomRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room_request = self.get_object(pk)
        serializer = RoomRequestSerializer(room_request)

        return Response(serializer.data)

    def put(self, request, pk):
        room_request = self.get_object(pk)
        serializer = self.get_serializer_class()(room_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room_request = self.get_object(pk)
        room_request.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
