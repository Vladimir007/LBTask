from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from shop.models import User

from .permissions import IsStaffOrTargetUser
from .serializers import UserSerializer



class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')

    def get_permissions(self):
        return [AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]


class UserLogoutView(LogoutView):
    def post(self, *args, **kwargs):
        return JsonResponse({})
