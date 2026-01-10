# blog_app/admin.py
from django.contrib import admin
from .models import Category, Post, Comment

# Remove Profile import from here
# Profile should be registered in users/admin.py

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
# Remove: admin.site.register(Profile)