from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign-up', views.register_view),
    path('sign-in', views.login_view),
    path('check-token', views.check_token),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]