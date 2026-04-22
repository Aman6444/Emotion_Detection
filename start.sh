#!/bin/bash

# Startup script for Railway deployment
# This ensures PORT is set before starting gunicorn

# Railway automatically sets PORT, but we'll add a fallback
PORT=${PORT:-5000}

echo "✅ Starting application on port $PORT"

# Start gunicorn with proper port binding
exec gunicorn --bind "0.0.0.0:$PORT" --workers 1 --threads 2 --timeout 120 --log-level info wsgi:app
