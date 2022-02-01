echo $pwd

cd source

# TODO fix 
sleep 10

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000