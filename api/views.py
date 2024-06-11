from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime

from api.serializer import RegistrationSerializer, ProfileSerializer, FriendsSerializer
from api.models import Profile, Friends
from api.permisions import IsOwner, IsRequestRecivedSent


from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import status

# Create your views here.


class SignupApiView(CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

class ProfileCreateListApiView(ListAPIView, CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


    def perform_create(self, serializer):
        return serializer.save(user_object = self.request.user)

class ProfileDestroyUpdatefetchview(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class FriendsRequestSend(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        friends_profile_object = Profile.objects.get(id=id)
        profile_object = Profile.objects.get(user_object=request.user)
        serializer_instance = FriendsSerializer(data=request.data)
        current_time = datetime.now()

        if profile_object.last_request_time:
            time_diff = current_time - profile_object.last_request_time
        else:
            time_diff = 0

        if serializer_instance.is_valid():
            if time_diff == 0 or time_diff.total_seconds() > 120:
                serializer_instance.save(user_object = profile_object, friends_object=friends_profile_object, request_sent=True)
                profile_object.last_request_time = current_time
                profile_object.save()
                message = {"success message": "Friend request sent successfully"}
                return Response(data=message, status=status.HTTP_201_CREATED)
            else:
                message = {"error message": "You have to wait for 2 minutes to send your friend request"}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

        
class FriendRequestRecivedList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        profile_user = Profile.objects.get(user_object = request.user)
        friends_object = Friends.objects.filter(friends_object=profile_user,request_sent = True)
        serializer_instance = FriendsSerializer(friends_object, many = True)
        print(serializer_instance)
        return Response(serializer_instance.data, status=status.HTTP_200_OK)

    
class FriendRequestDelete(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsRequestRecivedSent]
    def delete(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        Friends.objects.get(id=id).delete()
        return Response(status=status.HTTP_200_OK)

class FriendRequestAccept(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsRequestRecivedSent]
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        friend_object = Friends.objects.get(id=id)
        friend_object.is_friend = True
        friend_object.save()
        if friend_object:
            Friends.objects.create(
            friends_object = friend_object.user_object,
            user_object = friend_object.friends_object,
            recieved_request = True,
            is_friend = True,

        )
  
        return Response(data={"message":"accepted"}, status=status.HTTP_201_CREATED)

class FriendList(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendsSerializer


    def get_queryset(self):
        profile_obj = Profile.objects.get(user_object = self.request.user)
        return Friends.objects.filter(user_object =profile_obj, is_friend= True)
        

class Search(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get("search")
        if data:
            qs = Profile.objects.filter(user_object__username__contains = data)
        serializer_instance = ProfileSerializer(qs, many  =True)

        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
     

        


    



        






