from django.urls import path
from . import views

urlpatterns = [
    path('reminders/', views.user_reminders, name='user_reminders'),
    path('reminder/<int:reminder_id>/mark_sent/', views.mark_reminder_sent, name='mark_reminder_sent'),
    path('reminder/<int:reminder_id>/delete/', views.delete_reminder, name='delete_reminder'),
]
