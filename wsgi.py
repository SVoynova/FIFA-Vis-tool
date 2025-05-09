"""
Deployment entry point for the FIFA World Cup 2022 Visualization Dashboard
"""

# Import the Dash app from the app package
from app.main import app

# This is used by gunicorn in production
server = app.server

# For local development
if __name__ == "__main__":
    app.run(debug=False) 