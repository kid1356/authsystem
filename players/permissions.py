from rest_framework import permissions



class CaptainPermissions(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.roll == 'Captain'
    
class IsCaptainOfPlayer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.captain == request.user