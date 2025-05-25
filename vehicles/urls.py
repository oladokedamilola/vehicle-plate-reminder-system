from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('edit/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),


    path('my-vehicles/', views.user_vehicles, name='user_vehicles'),
]

