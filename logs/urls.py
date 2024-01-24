from django.urls import path
from . import views

urlpatterns = [
    path('invalid-pin', views.invalid_pin),
    path('delete-log/<int:log_id>', views.delete_log),
]