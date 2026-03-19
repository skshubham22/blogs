from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import Message, Friendship
from django.utils import timezone
from users.models import Notification

@login_required
def inbox(request):
    # Get all messages involving the user to find partners and last messages
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    partners_info = {} # user_id -> {last_message, unread_count}
    
    for msg in all_messages:
        partner = msg.receiver if msg.sender == request.user else msg.sender
        if partner.id not in partners_info:
            partners_info[partner.id] = {
                'user': partner,
                'last_message': msg,
                'unread_count': 0
            }
    
    # Calculate unread counts
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False)
    for msg in unread_messages:
        if msg.sender_id in partners_info:
            partners_info[msg.sender_id]['unread_count'] += 1
            
    # Sort by last message timestamp (already implicitly handled by the order of keys if we were using OrderedDict, but let's be safe)
    chat_list = list(partners_info.values())
    chat_list.sort(key=lambda x: x['last_message'].timestamp, reverse=True)
    
    # Get pending friend requests
    pending_requests = Friendship.objects.filter(user2=request.user, status='pending')
    
    return render(request, 'chat/inbox.html', {
        'chat_list': chat_list,
        'pending_requests': pending_requests,
        'today': timezone.now().date()
    })

@login_required
def send_friend_request(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user != request.user:
        # Check if friendship already exists
        exists = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=other_user)) |
            (Q(user1=other_user) & Q(user2=request.user))
        ).exists()
        if not exists:
            Friendship.objects.create(user1=request.user, user2=other_user, status='pending')
            Notification.objects.create(
                user=other_user,
                sender=request.user,
                notification_type='friend_request',
                content=f"{request.user.username} sent you a friend request.",
                related_object_id=request.user.id
            )
    return redirect('profile-user', username=username)

@login_required
def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, user2=request.user)
    friendship.status = 'accepted'
    friendship.save()
    return redirect('inbox')

@login_required
def direct_message(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'chat/direct.html', {
        'other_user': other_user,
        'chat_messages': messages
    })

@login_required
def api_get_messages(request, username):
    other_user = get_object_or_404(User, username=username)
    mode = request.GET.get('mode', 'unread')
    
    if mode == 'history':
        # Get last 20 messages between users
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('-timestamp')[:20]
        # Reverse to show oldest first
        messages = list(messages)[::-1]
    else:
        # Get only unread messages
        messages = Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).order_by('timestamp')
    
    # Mark received messages in this batch as read
    unread_ids = [m.id for m in messages if m.receiver == request.user and not m.is_read]
    if unread_ids:
        Message.objects.filter(id__in=unread_ids).update(is_read=True)
    
    data = []
    for msg in messages:
        data.append({
            'body': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'sender': msg.sender.username,
            'is_me': msg.sender == request.user
        })
    
    return JsonResponse({'messages': data})

from users.models import Notification, UserActivity

@login_required
def api_send_message(request, username):
    if request.method == 'POST':
        other_user = get_object_or_404(User, username=username)
        content = request.POST.get('body') 
        if content:
            msg = Message.objects.create(sender=request.user, receiver=other_user, content=content)
            
            # Log message activity
            UserActivity.objects.create(
                user=request.user,
                action='send_message',
                metadata={'receiver': other_user.username, 'content_preview': content[:50]},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({
                'status': 'ok',
                'body': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M')
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def api_get_conversations(request):
    # Get all messages involving the user
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    partners_seen = set()
    chat_list = []
    
    for msg in all_messages:
        partner = msg.receiver if msg.sender == request.user else msg.sender
        if partner.id not in partners_seen:
            partners_seen.add(partner.id)
            
            # Format timestamp
            timestamp = msg.timestamp.strftime('%b %d')
            if msg.timestamp.date() == timezone.now().date():
                timestamp = msg.timestamp.strftime('%H:%M')
                
            chat_list.append({
                'username': partner.username,
                'image': partner.profile.image.url if hasattr(partner, 'profile') else '/static/images/default.png',
                'last_message': msg.content[:30] + '...' if len(msg.content) > 30 else msg.content,
                'timestamp': timestamp,
                'is_read': msg.is_read or msg.sender == request.user,
                'sender_is_me': msg.sender == request.user
            })
            
            # Limit to last 10 conversations for the dropdown
            if len(chat_list) >= 10:
                break
    
    return JsonResponse({'conversations': chat_list})
