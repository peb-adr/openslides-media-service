#!/bin/bash

export DATABASE_HOST="${DATABASE_HOST:-db}"
export DATABASE_PORT="${DATABASE_PORT:-5432}"
export DATABASE_NAME="${DATABASE_NAME:-mediafiledata}"
export DATABASE_USER="${DATABASE_USER:-openslides}"
export DATABASE_PASSWORD="${DATABASE_PASSWORD:-openslides}"

until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT"; do
  echo "Waiting for Postgres server '$DATABASE_HOST' to become available..."
  sleep 3
done

# Create schema in postgresql
PGPASSWORD="$DATABASE_PASSWORD" psql -1 -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" -f src/schema.sql

exec "$@"
