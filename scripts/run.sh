#!/bin/sh

# Any command fails => exit script immediately.
set -e

# Wait for DB initialisation.
python manage.py wait_for_db

# Collect all the static files into a single directory.
python manage.py collectstatic --noinput

# Perform migrations.
python manage.py migrate

# Run UWSGI.
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
