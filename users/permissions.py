from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.is_superuser)


class IsClient(BasePermission):

    message = "Sorry but access only for clients"

    def has_permission(self, request, view):
        return bool(
            request.user.is_anonymous
            or request.user.role == 2
        )


class IsOrderClient(BasePermission):
    """
    Allows access only to client
    """

    edit_methods = "DELETE"

    message = "Sorry but access only for clients"

    def has_permission(self, request, view):
        return bool(
            request.user.is_anonymous
            or request.user.role == 2
            and request.method not in self.edit_methods

        )

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous or request.user.role == 2 and request.method not in self.edit_methods:
            return True
        return False