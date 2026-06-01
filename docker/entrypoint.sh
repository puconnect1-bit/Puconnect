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

# Start the application using daphne (ASGI)
echo "Starting Daphne server..."
exec daphne pu_mp.asgi:application --port 8000 --bind 0.0.0.0
