echo
echo Setup pipenv: global install for virtual environment management
echo
pip install pipenv
echo
echo Install dependencies: use pipenv to install dev dependencies
echo
pipenv install --dev
echo
echo Install DB: Using SQLite - no install required
echo
echo
echo Migrate DB: Use Django to migrate DB to latest version
echo
pipenv run ./manage.py migrate
echo
echo Setup seed: Use Django to load seed file with default data
echo
pipenv run ./manage.py loaddata story/fixture.json
echo
echo Check style: Use pylint to check coding style standards
echo
pipenv run pylint **/*.py
echo
echo Check types: Use mypy to check static type annotations
echo
pipenv run mypy **/*.py
echo
echo Check tests: Use unittest to check application functionality
echo
pipenv run ./manage.py test
