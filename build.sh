#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Populate data
# python populate_categories.py
# python populate_full_blog.py
python populate_internet_blogs.py
