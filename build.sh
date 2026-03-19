#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Populate data if needed (optional, uncomment if you want fresh data on deploy)
# python populate_categories.py
# python populate_full_blog.py

# TEMPORARY: Reset admin password for Render deployment
# Remove this after successful login
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
