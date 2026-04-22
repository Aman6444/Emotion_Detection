"""
WSGI entry point for Vercel deployment
"""
from app import app

# Vercel requires the app to be exposed as 'app'
# This is the entry point for serverless deployment
if __name__ == "__main__":
    app.run()
