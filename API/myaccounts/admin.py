from django.contrib import admin
from .models import User, Staff, Photographer, Client, Bookings, BookingHistory, JobPost, JobApplication,  WorkHistory

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Photographer)
admin.site.register(Client)


@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'photographer', 'event_date', 'status')
    list_filter = ('status', 'event_date', 'client')
    search_fields = ('client__username', 'photographer__username', 'event_date')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = User.objects.filter(user_type=3) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'booking', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('client__username', 'booking__title')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = User.objects.filter(user_type=3) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'title', 'event_date', 'created_at')
    list_filter = ('client__username', 'event_date', 'created_at')
    search_fields = ('client__username', 'title')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = User.objects.filter(user_type=3)  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(JobApplication)
class JobApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'photographer', 'job_post', 'client', 'message')
    list_filter = ('photographer__user__username', 'job_post__title', 'client__user__username')
    search_fields = ('photographer__user__username', 'job_post__title', 'client__user__username', 'message')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['photographer', 'client']:
            kwargs['queryset'] = User.objects.filter(user_type=2)  
            kwargs['queryset'] = User.objects.filter(user_type=3) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(WorkHistory)
class WorkHistoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'photographer', 'start_date', 'end_date', 'position')
    list_filter = ('photographer__username', 'start_date', 'end_date')
    search_fields = ('photographer__username', 'position')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'photographer':
            kwargs['queryset'] = User.objects.filter(user_type=2) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)