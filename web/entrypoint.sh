#!/bin/sh

# Apply database migrations
echo "Applying database migrations ..."
python manage.py migrate

# Create superuser
echo "Creating superuser ..."
python manage.py createsuperuser --noinput

# Load initial data (backup)
echo "Load initial data"
# python manage.py loaddata admin.json
# python manage.py dumpdata > admin.json для получения данных с тестовой версии

# Collecting static
echo "Collecting static ..."
python manage.py collectstatic

# Start server
echo "Starting server ..."
python manage.py runserver 0.0.0.0:8000
