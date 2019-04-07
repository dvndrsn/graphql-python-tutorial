from invoke import Collection, task


@task
def install_pipenv(context):
    """ Setup install pipenv: globally install pipenv """
    context.run("pip3 install pipenv")


@task
def install_dependencies(context):
    """ Setup install dependencies: install project dependencies to a virtual environemnt """
    context.run("pipenv install --dev")


@task(pre=[install_pipenv, install_dependencies])
def dependencies(context):
    """ Setup dependenciess: install pipenv and dependencies """


@task
def migrate_db(context):
    """ Setup migrate db: migrate database schema """
    context.run("pipenv run migrate_db")


@task
def seed_db(context):
    """ Setup migrate seed db: populate database with sample data """
    context.run("pipenv run setup_seed")


@task(pre=[migrate_db, seed_db])
def db(context):
    """ Setup db: migrate schema and load sample data """


@task(name='all', pre=[dependencies, db])
def all_(context):
    """ Setup dependencies and database """


@task
def superuser(context):
    """ Setup superuser: Create a superuser for the Django admin panel """
    context.run("pipenv run setup_superuser")


setup = Collection('setup')
setup.add_task(all_, default=True)
setup.add_task(install_pipenv)
setup.add_task(install_dependencies)
setup.add_task(seed_db)
setup.add_task(migrate_db)
setup.add_task(superuser)
