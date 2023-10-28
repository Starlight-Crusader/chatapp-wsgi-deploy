from django.urls import path
from . import views

urlpatterns = [
    path('get-contacts', views.GetContactsListView.as_view()),
    path('search-contacts', views.SearchContactsListView.as_view()),
    path('add-contact', views.add_contact),
    path('remove-contact', views.remove_contact)
]
