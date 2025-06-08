from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),

    path('settings/', views.update_settings, name='update_settings'),

    path('mark_read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/', views.user_notifications, name='user_notifications'),

]
