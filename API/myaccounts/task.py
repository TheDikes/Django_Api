from celery import shared_task
from datetime import timedelta
from .models import Bookings, Notification, Photographer


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



# Update the suspend_booking function to automatically decline the booking
def decline_booking(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    booking.status = 'Denied'
    booking.reason_for_denial = '24-hour review period expired'
    booking.save()

@shared_task
def start_booking_timer(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    """ Start the 24-hour timer for this booking
        Use Celery to schedule the task after 24 hours
    """
    check_booking_response.delay(booking_id)

@shared_task
def check_booking_response(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.status == 'Pending' and not booking.is_within_24_hours():
        """ Automatically decline the booking if no response within 24 hours """
        decline_booking(booking_id)
