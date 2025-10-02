#!/bin/bash

until nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done
echo "PostgreSQL is ready! Starting the server..."
exec "$@"