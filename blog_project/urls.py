"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# blog_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),
    
    # User Auth
    path('register/', user_views.register, name='register'),
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout'),
    
    # User Settings & Profile
    path('settings/', user_views.settings_view, name='settings'),
    path('profile/edit/', user_views.edit_profile, name='edit-profile'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/<str:username>/', user_views.profile, name='profile-user'),
    
    # Notifications & Search
    path('notification/<int:pk>/read/', user_views.mark_notification_as_read, name='mark-notification-read'),
    path('api/notifications/', user_views.api_get_notifications, name='api-notifications'),
    path('search-users/', user_views.search_users, name='search-users'),
    path('api/user-search/', user_views.api_user_search, name='api-user-search'),
    path('api/validate_username/', user_views.validate_username, name='validate-username'),
    
    # Chat
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)