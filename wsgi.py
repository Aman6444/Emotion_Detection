"""
WSGI entry point for production deployment
"""
import os
from app import app

# This is the entry point for gunicorn and other WSGI servers
# The app object is what gunicorn will use

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
