from django.contrib import admin

# Register your models here.
from .models import User, Staff, Photographer, Client, Bookings, BookingHistory, WorkHistory

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Photographer)
admin.site.register(Client)
admin.site.register(Bookings)
admin.site.register(BookingHistory)
admin.site.register(WorkHistory)
