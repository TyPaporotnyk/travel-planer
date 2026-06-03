#!/usr/bin/sh
set -e

echo "Apply migrations"
alembic upgrade head

echo "Starting application"
exec gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
