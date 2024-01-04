from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .models import Bookings
from .task import start_booking_timer

@receiver(post_save, sender=Notification)
def send_notification_to_photographer(sender, instance, created, **kwargs):
    if created:
        
        """ Send an email to the photographer """
        subject = "New Booking Notification"
        message = f"You have a new booking request. Please log in to your account to review and respond."
     

@receiver(post_save, sender=Bookings)
def create_booking_timer(sender, instance, created, **kwargs):
    if created:
        start_booking_timer.delay(instance.id)  # Start the 24-hour timer for the newly created booking
