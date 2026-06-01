#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Ensure staticfiles directory exists
mkdir -p /app/staticfiles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Execute the command passed to the container
exec "$@"
