#!/bin/sh

set -e

host="$DATABASE_URL"
port="5432"

until nc -z "$host" "$port"; do
  echo "Waiting for postgres..."
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

exec "$@"
