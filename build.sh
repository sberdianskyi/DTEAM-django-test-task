#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# To load the sample data into the project
python manage.py loaddata sample_data.json

# Run Celery worker in the background
celery -A CVProject worker --loglevel=info &
