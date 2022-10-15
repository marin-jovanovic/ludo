# activate venv
source venv/bin/activate

# to add new models
python3 manage.py makemigrations
python3 manage.py migrate

# run backend
python3 manage.py runserver
