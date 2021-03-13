from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
    Custom permission class
    """

    def has_object_permission(self, request, view, obj):
        """
        providing implementation for the method provided by
        BasePermission.
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return obj.students.filter(id=request.user.id).exists()
