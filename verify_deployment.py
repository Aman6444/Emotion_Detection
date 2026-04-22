"""
Pre-deployment verification script
Run this before deploying to ensure everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def check_env_var(var_name, required=False):
    """Check if environment variable is set"""
    value = os.environ.get(var_name)
    if value:
        print(f"✅ {var_name}: Set")
        return True
    else:
        if required:
            print(f"❌ {var_name}: Not set (Required for production)")
        else:
            print(f"⚠️  {var_name}: Not set (Optional)")
        return not required

def main():
    print("🔍 Pre-Deployment Verification\n")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check essential files
    print("\n📁 Checking Essential Files:")
    all_checks_passed &= check_file_exists("app.py", "Main application")
    all_checks_passed &= check_file_exists("wsgi.py", "WSGI entry point")
    all_checks_passed &= check_file_exists("requirements.txt", "Requirements file")
    all_checks_passed &= check_file_exists("emotiondetector.h5", "Model weights")
    all_checks_passed &= check_file_exists("emotiondetector.json", "Model architecture")
    
    # Check deployment files
    print("\n📦 Checking Deployment Files:")
    check_file_exists("Procfile", "Heroku Procfile")
    check_file_exists("Dockerfile", "Docker configuration")
    check_file_exists("runtime.txt", "Python version spec")
    check_file_exists(".gitignore", "Git ignore file")
    
    # Check template files
    print("\n🎨 Checking Template Files:")
    all_checks_passed &= check_file_exists("templates/landing.html", "Landing page")
    all_checks_passed &= check_file_exists("templates/detect.html", "Detection page")
    
    # Check static files
    print("\n🎭 Checking Static Files:")
    all_checks_passed &= check_file_exists("static/landing.css", "Landing CSS")
    all_checks_passed &= check_file_exists("static/style.css", "Main CSS")
    all_checks_passed &= check_file_exists("static/script.js", "JavaScript")
    
    # Check environment variables
    print("\n🔐 Checking Environment Variables:")
    check_env_var("FLASK_ENV")
    check_env_var("SECRET_KEY")
    check_env_var("PORT")
    
    # Check Python packages
    print("\n📚 Checking Python Packages:")
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask: Not installed")
        all_checks_passed = False
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV: Not installed")
        all_checks_passed = False
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow: {tf.__version__}")
    except ImportError:
        print("❌ TensorFlow: Not installed")
        all_checks_passed = False
    
    try:
        import keras
        print(f"✅ Keras: {keras.__version__}")
    except ImportError:
        print("❌ Keras: Not installed")
        all_checks_passed = False
    
    # Model file size check
    print("\n💾 Checking Model File Sizes:")
    if os.path.exists("emotiondetector.h5"):
        size_mb = os.path.getsize("emotiondetector.h5") / (1024 * 1024)
        print(f"📊 Model size: {size_mb:.2f} MB")
        if size_mb > 100:
            print("⚠️  Warning: Model file is large, may affect deployment")
    
    # Final report
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("✅ All critical checks passed!")
        print("🚀 Ready for deployment!")
        return 0
    else:
        print("❌ Some critical checks failed!")
        print("⚠️  Please fix the issues before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
