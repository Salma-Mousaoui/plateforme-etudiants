web: python manage.py collectstatic --noinput && python manage.py migrate --run-syncdb && daphne config.asgi:application --port $PORT --bind 0.0.0.0
