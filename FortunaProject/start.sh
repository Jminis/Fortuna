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
daphne -p 8000 FortunaProject.asgi:application

