#!/bin/bash
cd backend
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :10000) 2>/dev/null || true
gunicorn config.wsgi:application --bind 0.0.0.0:8000 > backend_output.log 2>&1 &
cd ../frontend
npm run preview -- --host 0.0.0.0 --port 10000 > frontend_output.log 2>&1 &
echo "Started"
