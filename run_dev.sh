#!/bin/bash
cd backend
gunicorn config.wsgi:application --bind 0.0.0.0:8000 &
PID_BACKEND=$!
cd ../frontend
npm run preview -- --host 0.0.0.0 --port 10000 &
PID_FRONTEND=$!
echo "Backend PID: $PID_BACKEND"
echo "Frontend PID: $PID_FRONTEND"
