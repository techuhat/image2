#!/usr/bin/env python3
"""
Production runner for Flask PDF Tools Backend
Optimized for Linux VPS deployment
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, logger

def check_system_dependencies():
    """Check and report system dependencies status"""
    dependencies = {
        'LibreOffice': 'libreoffice --version',
        'Ghostscript': 'gs --version',
        'Python': 'python3 --version'
    }
    
    missing = []
    
    for name, cmd in dependencies.items():
        try:
            import subprocess
            result = subprocess.run(cmd.split(), capture_output=True, timeout=5)
            if result.returncode != 0:
                missing.append(name)
            else:
                logger.info(f"✓ {name} is available")
        except:
            missing.append(name)
            logger.warning(f"✗ {name} not found")
    
    if missing:
        logger.warning(f"Missing system dependencies: {', '.join(missing)}")
        logger.info("Install commands for Ubuntu/Debian:")
        if 'LibreOffice' in missing:
            logger.info("  sudo apt-get update && sudo apt-get install -y libreoffice")
        if 'Ghostscript' in missing:
            logger.info("  sudo apt-get install -y ghostscript")
    
    return len(missing) == 0

def create_directories():
    """Create necessary directories"""
    directories = ['cache', 'temp', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    logger.info("Created necessary directories")

def main():
    """Main entry point for production"""
    logger.info("Starting Flask PDF Tools Backend")
    
    # Create directories
    create_directories()
    
    # Check system dependencies
    deps_ok = check_system_dependencies()
    if not deps_ok:
        logger.warning("Some system dependencies are missing. Some features may not work.")
    
    # Get configuration from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Server configuration: host={host}, port={port}, debug={debug}")
    
    if debug:
        # Development mode
        logger.info("Running in development mode")
        app.run(host=host, port=port, debug=True)
    else:
        # Production mode with gunicorn
        logger.info("Running in production mode with gunicorn")
        os.system(f'gunicorn --bind {host}:{port} --workers 4 --worker-class sync --timeout 300 --max-requests 1000 --preload app:app')

if __name__ == '__main__':
    main()
