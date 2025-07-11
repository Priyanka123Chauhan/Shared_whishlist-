from rest_framework.permissions import BasePermission

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by or request.user in obj.members.all()
