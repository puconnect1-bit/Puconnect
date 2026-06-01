#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for database if using Postgres
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    # Use a simple python script to check if the database is available
    python << END
import sys
import psycopg2
import time
import os

db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')

while True:
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        conn.close()
        break
    except psycopg2.OperationalError:
        time.sleep(0.1)
END
    echo "PostgreSQL started"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Automatically create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --no-input || echo "Superuser already exists."
fi

# Execute the command passed to the container
exec "$@"
