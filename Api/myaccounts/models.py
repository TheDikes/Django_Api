from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a user with the given email, first_name,
          last_name, username
          and password.
        """
        if not email:
            raise ValueError("Please provide a valid email")
        

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
     
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, username
        and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Staff"),
        (2, "Photographer"),
        (3, "Client"),
    )
    user_type = models.IntegerField(default=1, choices=USER_TYPE_CHOICES)

    email = models.EmailField(max_length=80, unique=True)
    username = models.CharField(max_length=45, unique=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUser()

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if instance is being created or updated
        super().save(*args, **kwargs)

        if created:  # If the instance is being created
            if self.user_type == 1:  # Staff
                Staff.objects.create(user=self)

            elif self.user_type == 2:  # Photographer
                Photographer.objects.create(user=self)

            elif self.user_type == 3:  # Client
                Client.objects.create(user=self)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')

    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"


class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='photographer')

    age = models.PositiveIntegerField(null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='photographer_images/')
    bio = models.TextField(help_text="The bio of the photographer")
    portfolio = models.FileField(upload_to='photographer_portfolios/', blank=True, null=True)
    portfolio_url = models.URLField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    social_link = models.URLField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=20, null=False)
    bank_name = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name = "Photographer"
        verbose_name_plural = "Photographers"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')

    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=50, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='client_images/')
    description = models.TextField(null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Bookings(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings', null=True)
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photographer_bookings', null=True)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.username} booking {self.photographer.username} for {self.event_date}"
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class BookingHistory(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_booking_history', null=True)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client: {self.client.username}, Booking History ID: {self.id}"
    
    class Meta:
        verbose_name = "Booking History"
        verbose_name_plural = "Booking Histories"



class WorkHistory(models.Model):
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photographer_work_history', null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.photographer.username} - Work History ID: {self.id}"
    
    class Meta:
        verbose_name = "Work History"
        verbose_name_plural = "Work Histories"
