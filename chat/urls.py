from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('direct/<str:username>/', views.direct_message, name='direct-message'),
    path('api/get_messages/<str:username>/', views.api_get_messages, name='api-get-messages'),
    path('api/send_message/<str:username>/', views.api_send_message, name='api-send-message'),
    path('friend-request/send/<str:username>/', views.send_friend_request, name='send-friend-request'),
    path('friend-request/accept/<int:friendship_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('api/conversations/', views.api_get_conversations, name='api-get-conversations'),
]
