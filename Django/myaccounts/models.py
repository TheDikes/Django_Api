from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a user with the given email, first_name,
          last_name, username
          and password.
        """
        if not email:
            raise ValueError('Email is required to create a user')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, 
        and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser=True")
        
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Staff"),
        (2, "Photographer"),
        (3, "Client"),
    )

    user_type = models.IntegerField(default=1, choices=USER_TYPE_CHOICES)
    profile_switch = models.OneToOneField('myaccounts.ProfileSwitch', on_delete=models.CASCADE, null=True, blank=True, related_name='related_user')

    email = models.EmailField(max_length=80, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    username = models.CharField(max_length=45, unique=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()


    def switch_profile(self, profile_type):
        if self.profile_switch:
            self.profile_switch.active_profile.profile_type = profile_type
            self.profile_switch.active_profile.save()
        else:
            """ Create a new profile switch entry """
            profile = Profile.objects.create(profile_type=profile_type)
            switch = ProfileSwitch.objects.create(user=self, active_profile=profile)
            self.profile_switch = switch
            self.save()

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if instance is being created or updated
        super().save(*args, **kwargs)

        if created:  
            if self.user_type == 1: 
                Staff.objects.create(user=self)

            elif self.user_type == 2:  
                Photographer.objects.create(user=self)

            elif self.user_type == 3:  
                Client.objects.create(user=self)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class Profile(models.Model):
      PROFILE_CHOICES = (
        (1, 'Photographer'),
        (2, 'Client'),
        )
      profile_type = models.IntegerField(choices=PROFILE_CHOICES)

      """ Common fields for both Photographer and Client profiles """
      phone = models.CharField(max_length=20, blank=True, null=True)
      location = models.CharField(max_length=50, null=True)
      image = models.ImageField(null=True, blank=True, upload_to='profile_images/')
      
      class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"  
        
class ProfileSwitch(models.Model):
    user = models.OneToOneField('myaccounts.User', on_delete=models.CASCADE, related_name='related_profile_switch')
    active_profile = models.ForeignKey('myaccounts.Profile', on_delete=models.CASCADE)


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
    bio = models.TextField(help_text="The bio of the photographer")
    portfolio = models.FileField(upload_to='photographer_portfolios/', blank=True, null=True)
    portfolio_url = models.URLField(max_length=200, blank=True, null=True)
    social_link = models.URLField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=20, null=False)
    bank_name = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name = "Photographer"
        verbose_name_plural = "Photographers"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    description = models.TextField(null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"



class Bookings(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
    ]
      
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings', null=True)
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photographer_bookings', null=True)
    photographer_profile = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    client_profile = models.ForeignKey(Client, on_delete=models.CASCADE)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=20)
    reason_for_denial = models.TextField(blank=True, null=True)


    def review_booking(self, status, reason_for_denial=None):
        if status == 'Accepted':
            self.status = 'Accepted'
            self.save()
        elif status == 'Denied':
            self.status = 'Denied'
            self.reason_for_denial = reason_for_denial
            self.save()
        else:
            raise ValueError('Invalid status provided')
        

    @classmethod
    def create_booking_and_notify_photographer(cls, client, photographer, event_date, location, description):
        booking = cls.objects.create(
            client=client, 
            photographer=photographer, 
            event_date=event_date, 
            location=location, 
            description=description
            )
        
        """ Create a notification for the photographer """
        Notification.objects.create(photographer=photographer, booking=booking)

    def __str__(self):
        return f"{self.client.username} booking {self.photographer.username} for {self.event_date}"
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class Notification(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    unanswered_count = models.IntegerField(default=0)


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


class JobPost(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_job_posts', null=True)
    client_profile = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Job Post by {self.client.username}: {self.title}"
    
    class Meta:
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"



class JobApplication(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
  

    def __str__(self):
        return f"{self.photographer.user.username} applying for {self.job_post.title}"
    
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
    

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
