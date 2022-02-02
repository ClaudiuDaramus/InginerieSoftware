sleep 10
echo pwd
cd source
python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000