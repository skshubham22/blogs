# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.timesince import timesince

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomLoginForm
from .models import Profile, Notification, UserActivity
from chat.models import Friendship
from django.db.models import Q
from blog_app.models import Post

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    if notification.notification_type == 'friend_request':
        return redirect('profile')
    elif notification.notification_type in ['post_like', 'post_comment']:
        return redirect('post-detail', pk=notification.related_object_id)
    
    return redirect('blog-home')

from django.utils.timesince import timesince

@login_required
def api_get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    data = []
    for n in notifications:
        data.append({
            'pk': n.pk,
            'content': n.content,
            'is_read': n.is_read,
            'sender_username': n.sender.username,
            'sender_image': n.sender.profile.image.url,
            'created_at': n.created_at.isoformat(),
            'created_at_formatted': timesince(n.created_at) + " ago",
        })
    
    return JsonResponse({
        'notifications': data,
        'unread_count': unread_count
    })

def search_users(request):
    query = request.GET.get('q')
    if query:
        # Log search activity
        UserActivity.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='user_search',
            metadata={'query': query},
            ip_address=request.META.get('REMOTE_ADDR')
        )
        # Maintain history list
        history = request.session.get('search_history', [])
        if query in history:
            history.remove(query)
        history.insert(0, query)
        request.session['search_history'] = history[:5]
        request.session['last_user_search'] = query
        
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()
    
    return render(request, 'users/search_users.html', {'users': users, 'query': query})

@login_required
def api_user_search(request):
    query = request.GET.get('q', '')
    if query:
        # Log search activity
        UserActivity.objects.create(
            user=request.user,
            action='api_user_search',
            metadata={'query': query},
            ip_address=request.META.get('REMOTE_ADDR')
        )
        users = User.objects.filter(username__icontains=query)[:5]
        data = []
        for u in users:
            data.append({
                'username': u.username,
                'image': u.profile.image.url,
                'follower_count': Friendship.objects.filter(
                    (Q(user1=u) | Q(user2=u)),
                    status='accepted'
                ).count()
            })
        return JsonResponse({'users': data})
    
    # If no query, return history
    history = request.session.get('search_history', [])
    return JsonResponse({'history': history})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You have been logged in automatically.')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    success_message = "You have been logged in successfully!"

class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    is_own_profile = (request.user == profile_user)
    
    # Handle friendship status for the profile being viewed
    friendship_status = None
    if not is_own_profile:
        friendship = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=profile_user)) |
            (Q(user1=profile_user) & Q(user2=request.user))
        ).first()
        if friendship:
            friendship_status = friendship.status

    friend_count = Friendship.objects.filter(
        (Q(user1=profile_user) | Q(user2=profile_user)),
        status='accepted'
    ).count()

    total_likes = 0
    for post in profile_user.post_set.all():
        total_likes += post.total_likes()

    tagged_posts = Post.objects.filter(tagged_users=profile_user).order_by('-date_posted')

    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'friendship_status': friendship_status,
        'posts': profile_user.post_set.all().order_by('-date_posted'),
        'post_count': profile_user.post_set.count(),
        'friend_count': friend_count,
        'total_likes': total_likes,
        'tagged_posts': tagged_posts,
    }

    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def settings_view(request):
    return render(request, 'users/settings.html')

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'This username is already taken. Please choose another.'
    return JsonResponse(data)