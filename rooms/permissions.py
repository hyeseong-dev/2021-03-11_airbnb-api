from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, room): # 메서드 이름이 object_permission`이어야함 그래야 room인자를 받아 올수 있음
        return room.user == request.user