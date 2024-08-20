#!/bin/sh

set -e

if [ -n "$DATABASE_URL" ]; then
    uri=$(echo $DATABASE_URL | sed -e 's/^[^:]*:\/\///g')
    user_pass=$(echo $uri | grep @ | cut -d@ -f1)
    host_port=$(echo $uri | sed -e 's/^.*@//g' | cut -d/ -f1)
    host=$(echo $host_port | sed -e 's/:.*//g')
    port=$(echo $host_port | sed -e 's/^.*://g')
else
    echo "DATABASE_URL is not set"
    exit 1
fi

until nc -z "$host" "$port"; do
  echo "Waiting for postgres at $host:$port..."
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

exec "$@"