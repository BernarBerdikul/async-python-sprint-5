#!/bin/sh
echo "Run migrations..."
alembic -c ./alembic.ini upgrade head

echo "Starting server..."
exec gunicorn --chdir src -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 src.main:app
