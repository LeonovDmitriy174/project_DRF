from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsMyMaterials(BasePermission):
    message = "Для доступа к данной информации, необходимо преобрести доступ"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
