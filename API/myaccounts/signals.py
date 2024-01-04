from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, User, Profile, Bookings
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal handler to create a Profile instance for every new User created."""
    if created:
        if instance.user_type in [2, 3]:  # Photographer or Client
            Profile.objects.create(user=instance, profile_type=instance.user_type)