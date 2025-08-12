# zag_project
# ZAG Members Management

## Quick setup

1. Create virtualenv & install requirements

bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


2. Copy `.env.example` to `.env` and set `SECRET_KEY` and `DEBUG`.

3. Run migrations & load fixtures

bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata members/fixtures/homecells_and_ministries.json


4. Create a superuser

bash
python manage.py createsuperuser


5. Run the dev server

bash
python manage.py runserver


6. Visit `http://127.0.0.1:8000/` and log in. Use the admin at `/admin` to approve superadmin requests and assign homecells/ministry leaders.
