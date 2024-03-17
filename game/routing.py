from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/table/<str:table_name>/', consumers.TablePlayer.as_asgi()),
]
