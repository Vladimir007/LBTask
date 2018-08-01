from django.contrib.auth.mixins import AccessMixin


class DocTypeAccessMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        available_types = request.user.available_types
        if available_types is None:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
