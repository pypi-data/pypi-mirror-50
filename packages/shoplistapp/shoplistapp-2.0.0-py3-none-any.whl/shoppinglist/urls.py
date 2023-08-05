from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_index, name='list_index'),
    path("list_details/<int:pk>/", views.list_details, name='list_details'),
    path("list_delete/<int:pk>/", views.list_delete, name='list_delete'),
    path("add", views.list_add, name='list_add'),
]
