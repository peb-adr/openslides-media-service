#!/bin/bash

export DATABASE_HOST="${DATABASE_HOST:-db}"
export DATABASE_PORT="${DATABASE_PORT:-5432}"
export DATABASE_NAME="${DATABASE_NAME:-mediafiledata}"
export DATABASE_USER="${DATABASE_USER:-openslides}"
export DATABASE_PASSWORD="${DATABASE_PASSWORD:-openslides}"
export DATABASE_TABLE="${DATABASE_TABLE:-mediafile_data}"

until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" \
    -U "$DATABASE_USER" -d "$DATABASE_NAME"
do
  echo "Waiting for Postgres server '$DATABASE_HOST' to become available..."
  sleep 3
done

# Create schema in postgresql
echo "INFO: Setting up table ${DATABASE_TABLE} in database ${DATABASE_NAME} for media file storage."
PGPASSWORD="$DATABASE_PASSWORD" psql -1 -vON_ERROR_STOP=1 \
  -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" \
  -d "$DATABASE_NAME" -vt="$DATABASE_TABLE" \
  -f src/schema.sql ||
{
  echo "ERROR: Setup of mediafile table ${DATABASE_TABLE} in database ${DATABASE_NAME} failed! Aborting."
  exit 23
}

exec "$@"
