#!/bin/bash
cd backend
kill $(lsof -t -i :8000) 2>/dev/null || true
export DEBUG=True
python manage.py runserver 0.0.0.0:8000 > backend_output.log 2>&1 &
echo "Started"
