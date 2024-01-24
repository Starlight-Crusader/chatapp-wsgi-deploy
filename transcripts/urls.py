from django.urls import path
from . import views

urlpatterns = [
    path('encrypt', views.EncryptTranscriptView.as_view()),
    path('decrypt', views.DecryptTranscriptView.as_view()),
]