#!/bin/sh
set -e

# Run migrations
echo "Running database migrations..."
poetry run alembic upgrade head

# Start application
echo "Starting server..."
exec poetry run start
