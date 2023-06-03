from rest_framework import permissions

ADD_METHODS = ('POST',)
EDIT_METHODS = ('PUT', 'PATCH', 'DELETE')


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsResponsibleUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                request.method in (ADD_METHODS + EDIT_METHODS)
                and request.user
                and request.user.is_authenticated
            )
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method not in EDIT_METHODS
            or (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_staff
            )
        )
