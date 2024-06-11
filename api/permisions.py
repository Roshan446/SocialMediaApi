from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user_object == request.user


class IsRequestRecivedSent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.friends_object == request.user
    



