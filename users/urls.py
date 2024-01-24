from django.urls import path
from . import views

urlpatterns = [
    path('change-nickname', views.change_nickname),
    path('delete/<int:user_id>', views.delete_user),
]