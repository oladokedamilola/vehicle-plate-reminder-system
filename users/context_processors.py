from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        return {
            'notifications_unread_count': unread_count,
            'recent_notifications': recent_notifications,
        }
    return {}
