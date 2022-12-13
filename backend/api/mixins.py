from rest_framework import permissions
from .permissions import IsStaffEditorPermission

class StaffEditorPermissionMixin():
  permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
  # permission_classes = []

class UserQuerySetMixin():
  user_field = 'user'
  def get_queryset(self, *args, **kwargs):
    user = self.request.user
    lookup_data = {}
    lookup_data[self.user_field] = user
    queryset = super().get_queryset(*args, **kwargs)
    if user.is_admin:
      return queryset
    return queryset.filter(**lookup_data)