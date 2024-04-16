#!/bin/bash

REDIS_PID=$(lsof -t -i:6379)
if [ ! -z "$REDIS_PID" ]; then
  echo "Killing Redis process on port 6379..."
  kill -9 $REDIS_PID
fi

DAPHNE_PID=$(lsof -t -i:8000)
if [ ! -z "$DAPHNE_PID" ]; then
  echo "Killing Daphne process on port 8000..."
  kill -9 $DAPHNE_PID
fi

echo "Starting Redis server in the background..."
nohup redis-server &>/dev/null &

python manage.py collectstatic 
echo "Starting Daphne server on port 8000..."
#nohup daphne -p 8000 -b 0.0.0.0 FortunaProject.asgi:application &>/dev/null &
#python3 manage.py runserver 0.0.0.0:8000

LOGFILE="$HOME/celery_beat.log"
mkdir -p $(dirname "$LOGFILE")
echo "Starting Celery Beat..."
nohup celery -A FortunaProject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler >> $LOGFILE 2>&1 &

LOG_DIR="$HOME/celery_logs"
mkdir -p $(dirname "$LOG_DIR")

echo "Starting Celery Worker and Beat..."
nohup celery -A FortunaProject worker -l info >> "$LOG_DIR" 2>&1 &
daphne -p 8000 -b 0.0.0.0 FortunaProject.asgi:application
