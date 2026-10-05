#!/bin/sh
set -e

# La base ya está lista: docker compose espera el healthcheck de db (depends_on)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Superusuario opcional, se crea solo si las variables están definidas.
# Si ya existe, createsuperuser falla y se ignora (|| true).
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" || true
fi

exec "$@"
