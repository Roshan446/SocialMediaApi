from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender_choices = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other")
    )
    gender = models.CharField(max_length=10, choices=gender_choices)

    country = models.CharField(max_length=20)
    user_object = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    last_request_time = models.DateTimeField(blank=True, null=True)


class Friends(models.Model):
    friends_object = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_object = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_friends')
    request_sent = models.BooleanField(default=False)
    recieved_request = models.BooleanField(default=False)
    is_friend = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)











