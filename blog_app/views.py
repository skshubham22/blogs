# blog_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment, Category, PostImage
from users.models import Notification

# ... (rest of the imports)

from .forms import PostForm, CommentForm
from django.db.models import Q
from django.urls import reverse

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Handle additional images
        images = self.request.FILES.getlist('extra_images')
        for img in images:
            PostImage.objects.create(post=self.object, image=img)
            
        # Notify tagged users
        tagged_users = form.cleaned_data.get('tagged_users')
        if tagged_users:
            for user in tagged_users:
                if user != self.request.user:
                    Notification.objects.create(
                        user=user,
                        sender=self.request.user,
                        notification_type='post_tag',
                        content=f"{self.request.user.username} tagged you in a post: {self.object.title}",
                        related_object_id=self.object.pk
                    )
            
        messages.success(self.request, 'Your post has been created!')
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Get existing tagged users to avoid duplicate notifications on update
        existing_tagged = list(self.get_object().tagged_users.all())
        
        response = super().form_valid(form)
        
        # Handle additional images
        images = self.request.FILES.getlist('extra_images')
        for img in images:
            PostImage.objects.create(post=self.object, image=img)
            
        # Notify NEWLY tagged users
        new_tagged = form.cleaned_data.get('tagged_users')
        if new_tagged:
            for user in new_tagged:
                if user not in existing_tagged and user != self.request.user:
                    Notification.objects.create(
                        user=user,
                        sender=self.request.user,
                        notification_type='post_tag',
                        content=f"{self.request.user.username} tagged you in a post: {self.object.title}",
                        related_object_id=self.object.pk
                    )
            
        messages.success(self.request, 'Your post has been updated!')
        return response
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
from django.db.models import Q
from django.urls import reverse

@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog_app/home.html', context)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.user != post.author:
                Notification.objects.create(
                    user=post.author,
                    sender=request.user,
                    notification_type='post_comment',
                    content=f"{request.user.username} commented on your post: {post.title}",
                    related_object_id=post.pk
                )
            messages.success(request, 'Your comment has been added!')
    return redirect('post-detail', pk=post.pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notification_type='post_like',
                content=f"{request.user.username} liked your post: {post.title}",
                related_object_id=post.pk
            )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes()
        })
    
    return redirect('post-detail', pk=post.pk)

@login_required
def about(request):
    return render(request, 'blog_app/about.html')

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog_app/comment_form.html'
    
    def form_valid(self, form):
        # Additional check in case form is submitted late
        if not self.get_object().is_within_edit_window:
            messages.error(self.request, "Edit time limit exceeded (5 minutes).")
            return redirect('post-detail', pk=self.get_object().post.pk)
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
             if comment.is_within_edit_window:
                 return True
        return False
        
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk}) + "#comments"

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog_app/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user == comment.post.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk}) + "#comments"