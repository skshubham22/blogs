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
python manage.py shell -c "from django.contrib.auth.models import User; names = ['admin', 'shubham']; [ (u := User.objects.get_or_create(username=n, defaults={'is_superuser': True, 'is_staff': True})[0], u.set_password('admin123'), setattr(u, 'is_superuser', True), setattr(u, 'is_staff', True), u.save()) for n in names ]; print('Admin users updated')"
