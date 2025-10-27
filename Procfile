web: gunicorn quantumqr.wsgi --log-file -
release: python manage.py migrate
worker: celery -A quantumqr worker --loglevel=info

