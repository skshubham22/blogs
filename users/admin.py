# users/admin.py
from django.contrib import admin
from .models import Profile, Notification, UserActivity

admin.site.register(Profile)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('sender__username', 'user__username', 'content')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'action', 'metadata')
    readonly_fields = ('user', 'action', 'metadata', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False