#!/bin/bash

echo "🚀 Starting main_producer.py..."
python /app/main_producer.py &

echo "🔐 Starting SSH server..."
exec /usr/sbin/sshd -D
