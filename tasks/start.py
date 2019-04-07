from invoke import Collection, task


@task
def dev_server(context):
    """ Start development server: Use Django to start a hot-reloaded development server """
    context.run("pipenv run start", pty=True)


@task
def terminal_shell(context):
    """ Start terminal shell: Start pipenv terminal shell with dependencies activated in a virtual environment """
    print("Use: pipenv shell")


@task
def django_shell(context):
    """ Start django shell: Start a Django REPL to run commands interactively """
    context.run("pipenv run django_shell", pty=True)


start = Collection('start')
start.add_task(dev_server, default=True)
start.add_task(terminal_shell)
start.add_task(django_shell)
