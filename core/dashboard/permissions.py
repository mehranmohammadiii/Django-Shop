from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType

class HasAdminAccesPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.type == UserType.ADMIN.value

class HasCustomerAccesPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.type == UserType.CUSTOMER.value