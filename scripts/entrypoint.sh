#!/usr/bin/env bash

set -e
RUN_MANAGE_PY='poetry run python project/manage.py'

echo "Running migrations..."
$RUN_MANAGE_PY migrate --no-input

echo "Creating default Admin..."
$RUN_MANAGE_PY createdefaultadmin

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input
exec "$@"