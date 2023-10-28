from django.urls import path
from . import views

urlpatterns = [
    path('change-password', views.change_password),
    path('change-nickname', views.change_nickname),
    path('delete', views.delete_user),
    path('go-online', views.go_online),
    path('go-offline', views.go_offline),
]