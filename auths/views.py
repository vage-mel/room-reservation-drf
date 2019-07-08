from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from .serializers import *
from .permissions import IsOwnerOrIsStaffOrReadOnly


class ChoiceUserSerializerMixin:
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserFullSerializer
        return UserSerializer


class UserList(APIView, ChoiceUserSerializerMixin):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        users = User.objects.all().order_by('username')
        serializer = self.get_serializer_class()(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView, ChoiceUserSerializerMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrIsStaffOrReadOnly
    )

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = self.get_serializer_class()(user)

        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = self.get_serializer_class()(user, data=request.data,  partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMe(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data)
