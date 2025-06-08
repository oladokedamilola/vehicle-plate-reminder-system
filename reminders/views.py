from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from datetime import date
from .models import Reminder


from datetime import date


@login_required
def user_reminders(request):
    reminders = Reminder.objects.filter(user=request.user).select_related('vehicle').order_by('reminder_date')
    
    today = date.today()
    status_filter = request.GET.get('status')

    # Handle custom filter logic
    if status_filter == 'pending':
        reminders = reminders.filter(status='pending', reminder_date__gte=today)
    elif status_filter == 'sent':
        reminders = reminders.filter(status='sent')
    elif status_filter == 'expired':
        reminders = reminders.filter(status='pending', reminder_date__lt=today)
    elif status_filter == 'upcoming':
        reminders = reminders.filter(status='pending', reminder_date__gte=today)

    # Annotate each reminder with `days_left`
    reminders_list = list(reminders)
    for reminder in reminders_list:
        reminder.days_left = (reminder.reminder_date - today).days

    paginator = Paginator(reminders_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reminders': page_obj,
        'today': today,
        'status_filter': status_filter,
    }
    return render(request, 'reminders/user_reminders.html', context)




@login_required
@require_POST
def mark_reminder_sent(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if reminder.status != 'pending':
        return JsonResponse({'error': 'Reminder already marked as sent.'}, status=400)

    reminder.status = 'sent'
    reminder.save()
    return JsonResponse({'success': True, 'message': 'Reminder marked as sent.'})


@login_required
@require_POST
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.delete()
    return JsonResponse({'success': True, 'message': 'Reminder deleted.'})
