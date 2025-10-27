#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (optional - uncomment to create)
# python manage.py createsuperuser

# Start Django development server
python manage.py runserver

