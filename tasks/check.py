from invoke import Collection, task


@task
def style(context):
    """ Check style: Use pylint to check coding style standards """
    context.run("pipenv run check_style", pty=True)


@task
def types(context):
    """ Check types: Use mypy to check static type annotations """
    context.run("pipenv run check_types", pty=True)


@task(pre=[style, types])
def lint(context):
    """ lint: Check style and types """


@task
def tests(context):
    """ Check tests: Use unittest to check application functionality """
    context.run("pipenv run test", pty=True)


@task(name='all', pre=[style, types, tests])
def all_(context):
    """ Check style, types and tests """


check = Collection('check')
check.add_task(all_, default=True)
check.add_task(style)
check.add_task(types)
check.add_task(tests)
