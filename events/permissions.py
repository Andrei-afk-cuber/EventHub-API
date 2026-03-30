from rest_framework.permissions import BasePermission, SAFE_METHODS


# organizer permission
class IsOrganizerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True

        if view.action == 'create_book':
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_organizer

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        breakpoint()
        if request.method in SAFE_METHODS:
            return True

        return obj.organizer == request.user