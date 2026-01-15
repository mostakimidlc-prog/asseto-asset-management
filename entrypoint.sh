#!/bin/sh
# -------------------------------
# Assetto Asset Management EntryPoint
# -------------------------------

# Fail on errors
set -e

# Export Django settings if not already
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-AssetManagement.settings}

# Wait for Postgres to be ready
echo "Waiting for Postgres at $DATABASE_HOST:$DATABASE_PORT ..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done
echo "Postgres is up - continuing ..."

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Start server
echo "Starting Django server..."
gunicorn AssetManagement.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
