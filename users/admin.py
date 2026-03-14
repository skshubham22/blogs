# users/admin.py
from django.contrib import admin
from .models import Profile, Notification

admin.site.register(Profile)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('sender__username', 'user__username', 'content')