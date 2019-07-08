from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from room.views import *
from auths.views import *

urlpatterns = [
    path('api/token/', obtain_auth_token),

    path('api/users/', UserList.as_view()),
    path('api/users/<int:pk>/', UserDetail.as_view()),
    path('api/users/me/', UserMe.as_view()),

    path('api/rooms/', RoomList.as_view()),
    path('api/rooms/<int:pk>/', RoomDetail.as_view()),
    path('api/rooms/<int:room_id>/requests/',RoomRequestList.as_view()),

    path('api/requests/', RoomRequestList.as_view()),
    path('api/requests/<int:pk>/', RoomRequestDetail.as_view()),
]
