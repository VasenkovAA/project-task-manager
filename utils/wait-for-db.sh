#!/bin/sh

until pg_isready -h $DB_HOST -U $DB_USER -d $DB_NAME; do
  echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT with user $DB_USER and db $DB_NAME..."
  sleep 2
done
echo "PostgreSQL is ready!"