from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnProfilePermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_main)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PUT", "PATCH"]:
            return bool(obj.profile == request.user.profile)

        return False
