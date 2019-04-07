from invoke import Collection, task


@task
def db(context):
    """ Clean DB: Using Django to remove all local data """
    context.run("pipenv run python manage.py flush")


@task
def dependencies(context):
    """ Clean dependencies: Using pipenv to remove virtual environment """
    context.run("pipenv --rm")


@task(name='all', pre=[db, dependencies])
def all_(context):
    """ Clean all: return db and dependences to a clean local environment"""


clean = Collection('clean')
clean.add_task(all_, default=True)
clean.add_task(db)
clean.add_task(dependencies)
