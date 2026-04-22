"""
Vercel-compatible Flask app
This is a simplified version that works within Vercel's limits
"""
from flask import Flask, render_template, jsonify
import os
from pathlib import Path

# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route('/')
def index():
    """Landing page"""
    try:
        return render_template('landing.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'template_folder': app.template_folder,
            'static_folder': app.static_folder
        }), 500

@app.route('/detect')
def detect():
    """Detection page - Note: Webcam streaming not supported on Vercel"""
    try:
        return render_template('detect-vercel.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'template_folder': app.template_folder
        }), 500

@app.route('/video_feed')
def video_feed():
    """Video feed endpoint - Not supported on Vercel serverless"""
    return jsonify({
        'error': 'Video streaming not supported',
        'message': 'Vercel serverless functions cannot stream video. Please deploy to Render.com or Railway.app for full functionality.',
        'alternatives': [
            'Deploy to Render.com: https://render.com',
            'Deploy to Railway.app: https://railway.app',
            'Run locally: python app.py'
        ]
    }), 501

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'vercel',
        'note': 'Webcam streaming not supported on serverless platform'
    })

@app.route('/api/info')
def info():
    """API information"""
    return jsonify({
        'message': 'Face Emotion Detection API',
        'version': '1.0.0',
        'platform': 'Vercel Serverless',
        'limitations': [
            'Webcam streaming not supported',
            'Real-time video processing not available',
            'Consider deploying to Render.com or Railway.app for full functionality'
        ],
        'endpoints': {
            '/': 'Landing page',
            '/detect': 'Detection page (limited on Vercel)',
            '/health': 'Health check',
            '/api/info': 'This endpoint'
        }
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# Vercel requires this
if __name__ == '__main__':
    app.run()
