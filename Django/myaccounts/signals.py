from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification_to_photographer(sender, instance, created, **kwargs):
    if created:
        
        """ Send an email to the photographer """
        subject = "New Booking Notification"
        message = f"You have a new booking request. Please log in to your account to review and respond."
        # Send email logic here
