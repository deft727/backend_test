Start project


git clone https://github.com/deft727/backend_test.git

virtualenv - python -m venv venv

pip install -r requirements.txt - install requirements

createdb test_db - create PostgreSQL database

python manage.py createsuperuser

python manage.py migrate - migrate database

python manage.py runserver - run development server
