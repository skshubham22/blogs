# check_models.py
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

print("Checking models...")

# Check blog_app models
try:
    from blog_app.models import Category, Post, Comment
    print("[v] blog_app.models contains: Category, Post, Comment")
except ImportError as e:
    print(f"[x] blog_app.models import error: {e}")

# Check for Profile in blog_app (should NOT be there)
try:
    from blog_app.models import Profile
    print("[x] ERROR: Profile found in blog_app.models - remove it!")
except ImportError:
    print("[v] Profile NOT in blog_app.models - good!")

# Check users models
try:
    from users.models import Profile
    print("[v] users.models contains: Profile")
except ImportError as e:
    print(f"[x] users.models import error: {e}")

# List all models
from django.apps import apps
print("\nAll registered models:")
for model in apps.get_models():
    print(f"  - {model._meta.app_label}.{model.__name__}")