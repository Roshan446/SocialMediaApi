from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Friends, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "email", "password"]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user_object = serializers.StringRelatedField()
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["user_object", "id"]




class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = "__all__"
        read_only_fields = ["friends_object", "user_object"]



    
