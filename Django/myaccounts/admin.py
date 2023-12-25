from django.contrib import admin
from .models import User, Staff, Photographer, Client, Bookings, BookingHistory, JobPost, JobApplication,  WorkHistory

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Photographer)
admin.site.register(Client)


@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'photographer', 'event_date', 'status')
    list_filter = ('status', 'event_date')
    search_fields = ('client__username', 'photographer__username', 'event_date')


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'booking', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('client__username', 'booking__title')


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'title', 'event_date', 'created_at')
    list_filter = ('client__username', 'event_date', 'created_at')
    search_fields = ('client__username', 'title')



@admin.register(JobApplication)
class JobApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'photographer', 'job_post', 'client', 'message')
    list_filter = ('photographer__user__username', 'job_post__title', 'client__user__username')
    search_fields = ('photographer__user__username', 'job_post__title', 'client__user__username', 'message')

@admin.register(WorkHistory)
class WorkHistoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'photographer', 'start_date', 'end_date', 'position')
    list_filter = ('photographer__username', 'start_date', 'end_date')
    search_fields = ('photographer__username', 'position')