#!/bin/bash

# SOCIAL EXPERTS Django - Quick Start Script
# This script sets up the Django project for development

echo "================================================"
echo "  SOCIAL EXPERTS - Django Quick Start Setup"
echo "================================================"
echo ""

# Check Python version
echo "✓ Checking Python installation..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $python_version"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  Dependencies installed successfully"
echo ""

# Run migrations
echo "✓ Running database migrations..."
python manage.py migrate --no-input
echo "  Database initialized"
echo ""

# Collect static files
echo "✓ Collecting static files..."
python manage.py collectstatic --no-input -q
echo "  Static files collected"
echo ""

# Create superuser if needed
echo "✓ Django setup complete!"
echo ""
echo "================================================"
echo "  Next Steps:"
echo "================================================"
echo "1. Create a superuser account (admin):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Visit:"
echo "   - Main site: http://127.0.0.1:8000"
echo "   - Admin: http://127.0.0.1:8000/admin"
echo ""
echo "================================================"
