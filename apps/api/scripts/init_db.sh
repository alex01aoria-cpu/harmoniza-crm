#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Running migrations..."
cd /app
uv run alembic upgrade head

echo "Bootstrapping admin user..."
uv run python scripts/bootstrap_admin.py

echo "Database initialization complete!"

