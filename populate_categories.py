import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog_app.models import Category

categories = [
    'Technology', 'Lifestyle', 'Travel', 'Food', 'Health', 'Science', 
    'Education', 'Business', 'Entertainment', 'Sports'
]

for name in categories:
    Category.objects.get_or_create(name=name)
    print(f"Ensured category: {name}")

print("Categories populated.")
