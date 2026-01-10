# create_sample_data.py
from django.contrib.auth.models import User
from blog_app.models import Category, Post
from users.models import Profile

# Create categories
categories = ['Technology', 'Lifestyle', 'Travel', 'Food', 'Education']
for cat in categories:
    Category.objects.get_or_create(name=cat)

# Create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'password': 'testpass123'
    }
)
user.set_password('testpass123')
user.save()

