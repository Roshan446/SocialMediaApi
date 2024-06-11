from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("signup/", views.SignupApiView.as_view()),
    path("profile/", views.ProfileCreateListApiView.as_view()),
    path("profile/<int:pk>/", views.ProfileDestroyUpdatefetchview.as_view()),
    path("friend/send/request/<int:pk>/", views.FriendsRequestSend.as_view()),
    path("friend/requests/list/", views.FriendRequestRecivedList.as_view()),
    path("friend/request/accept/<int:pk>/", views.FriendRequestAccept.as_view()),
    path("friend/request/decline/<int:pk>/", views.FriendRequestDelete.as_view()),
    path("friends/list/", views.FriendList.as_view()),
    path("friends/search/", views.Search.as_view()),
    path("auth/token/", ObtainAuthToken.as_view()),




]
