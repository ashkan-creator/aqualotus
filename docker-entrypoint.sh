#!/bin/bash
set -e

echo "در حال اجرای mongod..."
mongod --dbpath /data/db --bind_ip 127.0.0.1 &
MONGO_PID=$!

echo "منتظر آماده شدن MongoDB..."
until mongosh --quiet --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1; do
  sleep 1
done
echo "MongoDB آماده است."

echo "اجرای سرور Node..."
exec node backend/server.js
