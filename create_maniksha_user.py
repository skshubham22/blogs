import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'manikshayadav'
password = 'Password123!'
email = 'maniksha@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username, email, password)
    print(f"User '{username}' created successfully.")
else:
    print(f"User '{username}' already exists.")
