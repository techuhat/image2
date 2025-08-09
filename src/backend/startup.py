#!/usr/bin/env python3
"""
Azure App Service startup script
This file is used by Azure to start the Flask application
"""
import os
import sys
from app import app

if __name__ == '__main__':
    # Azure App Service specific configuration
    port = int(os.environ.get('PORT', 8000))
    
    # Development mode for Azure
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True
        )
    else:
        # Production mode - let gunicorn handle this
        # This file is mainly for local testing
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
