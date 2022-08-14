release: python manage.py migrate
web: gunicorn cleanform.wsgi
worker: celery -A cleanform worker -E -l INFO