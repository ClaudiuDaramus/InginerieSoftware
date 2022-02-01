. .env
exec "$@"
cd source

# TODO
sleep 10

celery -A source worker -l info