from celery import shared_task
from datetime import timedelta
from .models import Notification
from .models import Photographer


def suspend_photographer(photographer_id):
    photographer = Photographer.objects.get(id=photographer_id)
    photographer.is_suspended = True
    photographer.save()


@shared_task
def start_notification_timer(notification_id):
    notification = Notification.objects.get(id=notification_id)
    """ Start the 24-hour timer for this notification
        Use Celery to schedule the task after 24 hours
    """
    check_response.delay(notification_id)

@shared_task
def check_response(notification_id):
    notification = Notification.objects.get(id=notification_id)
    if not notification.is_read:
        notification.unanswered_count += 1
        notification.save()

        if notification.unanswered_count >= 3:
            """ Call management command to suspend the photographer """
            suspend_photographer(notification.photographer)
