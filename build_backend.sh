#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_data || true
