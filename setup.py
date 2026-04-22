#!/usr/bin/env python3
"""
Setup and Verification Script for Face Emotion Detection App
This script checks prerequisites and sets up the environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_python_version():
    """Check if Python version is 3.10 or higher"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python 3.10+ required, found {version.major}.{version.minor}.{version.micro}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description} found: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if Path(dirpath).is_dir():
        print_success(f"{description} found: {dirpath}")
        return True
    else:
        print_error(f"{description} not found: {dirpath}")
        return False

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    print_info("Checking environment configuration...")
    if Path('.env').exists():
        print_success(".env file already exists")
        return True
    elif Path('.env.example').exists():
        print_warning(".env file not found, creating from template...")
        try:
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print_success(".env file created successfully")
            print_warning("Please update .env file with your configuration!")
            return True
        except Exception as e:
            print_error(f"Failed to create .env file: {e}")
            return False
    else:
        print_error(".env.example not found")
        return False

def check_virtual_environment():
    """Check if running in a virtual environment"""
    print_info("Checking virtual environment...")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print_success("Running in virtual environment")
        return True
    else:
        print_warning("Not running in virtual environment")
        print_info("Recommended: Create and activate a virtual environment")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_info("Checking Python dependencies...")
    required_packages = [
        'flask',
        'tensorflow',
        'keras',
        'opencv-python',
        'numpy',
        'pandas',
        'gunicorn',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"\nMissing packages: {', '.join(missing_packages)}")
        print_info("Run: pip install -r requirements.txt")
        return False
    else:
        print_success("All required packages installed")
        return True

def check_model_files():
    """Check if model files exist and are valid"""
    print_info("Checking ML model files...")
    
    checks = []
    checks.append(check_file_exists('emotiondetector.json', 'Model architecture'))
    checks.append(check_file_exists('emotiondetector.h5', 'Model weights'))
    
    # Check file sizes
    if Path('emotiondetector.h5').exists():
        size_mb = Path('emotiondetector.h5').stat().st_size / (1024 * 1024)
        if size_mb > 0.1:  # Should be at least 100KB
            print_success(f"Model weights file size: {size_mb:.2f} MB")
        else:
            print_error(f"Model weights file too small: {size_mb:.2f} MB")
            checks.append(False)
    
    return all(checks)

def check_project_structure():
    """Check if all required directories and files exist"""
    print_info("Checking project structure...")
    
    checks = []
    
    # Core files
    checks.append(check_file_exists('app.py', 'Main application'))
    checks.append(check_file_exists('wsgi.py', 'WSGI entry point'))
    checks.append(check_file_exists('config.py', 'Configuration'))
    checks.append(check_file_exists('requirements.txt', 'Requirements'))
    
    # Directories
    checks.append(check_directory_exists('templates', 'Templates directory'))
    checks.append(check_directory_exists('static', 'Static files directory'))
    
    # Template files
    if Path('templates').is_dir():
        checks.append(check_file_exists('templates/landing.html', 'Landing page'))
        checks.append(check_file_exists('templates/detect.html', 'Detection page'))
    
    # Static files
    if Path('static').is_dir():
        checks.append(check_file_exists('static/landing.css', 'Landing CSS'))
        checks.append(check_file_exists('static/style.css', 'Style CSS'))
        checks.append(check_file_exists('static/script.js', 'JavaScript'))
    
    return all(checks)

def check_port_availability(port=5000):
    """Check if the default port is available"""
    print_info(f"Checking port {port} availability...")
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            print_success(f"Port {port} is available")
            return True
    except OSError:
        print_warning(f"Port {port} is already in use")
        print_info("You can change the port in .env file or app.py")
        return False

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print_info("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def print_system_info():
    """Print system information"""
    print_info("System Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")

def main():
    """Main setup and verification function"""
    print_header("Face Emotion Detection - Setup & Verification")
    
    print_system_info()
    
    # Track all checks
    all_checks = []
    
    # 1. Check Python version
    print_header("1. Python Version Check")
    all_checks.append(check_python_version())
    
    # 2. Check virtual environment
    print_header("2. Virtual Environment Check")
    check_virtual_environment()  # Warning only, not critical
    
    # 3. Check project structure
    print_header("3. Project Structure Check")
    all_checks.append(check_project_structure())
    
    # 4. Check model files
    print_header("4. Model Files Check")
    all_checks.append(check_model_files())
    
    # 5. Create .env file
    print_header("5. Environment Configuration")
    all_checks.append(create_env_file())
    
    # 6. Check dependencies
    print_header("6. Dependencies Check")
    deps_installed = check_dependencies()
    if not deps_installed:
        print_info("\nWould you like to install dependencies now? (y/n)")
        try:
            response = input().strip().lower()
            if response == 'y':
                deps_installed = install_dependencies()
        except KeyboardInterrupt:
            print("\n\nSetup interrupted by user")
            sys.exit(1)
    all_checks.append(deps_installed)
    
    # 7. Check port availability
    print_header("7. Port Availability Check")
    check_port_availability()  # Warning only, not critical
    
    # Final summary
    print_header("Setup Summary")
    
    if all(all_checks):
        print_success("✓ All critical checks passed!")
        print_info("\nYou're ready to start the application:")
        print(f"\n  {Colors.BOLD}python app.py{Colors.END}")
        print(f"  or")
        print(f"  {Colors.BOLD}./start.sh{Colors.END} (Linux/Mac)")
        print(f"  {Colors.BOLD}start.bat{Colors.END} (Windows)\n")
        print_info("Access the app at: http://localhost:5000")
        return 0
    else:
        print_error("✗ Some checks failed!")
        print_info("\nPlease fix the issues above before running the application.")
        print_info("For help, check README.md or QUICKSTART.md")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
