from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework import routers

from .views import UserLogoutView, UserView


router = routers.DefaultRouter()
router.register('accounts', UserView, 'accounts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]
