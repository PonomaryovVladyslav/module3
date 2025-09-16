from django.contrib.auth.mixins import UserPassesTestMixin


class AdminPassTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class NonAdminPassTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_superuser


class RequestToFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
