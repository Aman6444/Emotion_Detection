#!/bin/bash

# Startup script for Railway deployment
# This ensures PORT is set before starting gunicorn

# Set default PORT if not provided by Railway
if [ -z "$PORT" ]; then
    echo "⚠️  PORT not set, using default 5000"
    export PORT=5000
else
    echo "✅ Using PORT: $PORT"
fi

# Start gunicorn
echo "🚀 Starting gunicorn on 0.0.0.0:$PORT"
exec gunicorn --bind "0.0.0.0:$PORT" --workers 1 --threads 2 --timeout 120 wsgi:app
