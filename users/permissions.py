from rest_framework.permissions import BasePermission


class IsBuyerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_buyer)

class IsSellerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_seller)
class IsSellerOrAdmin(BasePermission):
    """
    Allows access to product listing only to sellers or admins.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_seller or request.user.is_staff)

# In your view's `get_permissions` method:
def get_permissions(self):
    return [IsSellerOrAdmin()]