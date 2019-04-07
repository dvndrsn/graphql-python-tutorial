# GraphQL Python Tutorial

This tutorial will focus on building a GraphQL API using the Python library Graphene with a Django backend as a vehicle for teaching the principals of evolutionary API. This method can be applied across any tech stack, including REST, as well as the more practical concerns of working with Graphene and designing your API for GraphQL.

The majority of exercises and material for the tutorial is in this project, but there is also a [companion frontend project][tutorial-frontend]. That project can be used as a demo frontend for each backend exercise and is used in a later frontend-only exercise. See the slides [here][tutorial-slides].

[tutorial-frontend]: https://github.com/dvndrsn/graphql-python-tutorial-frontend/
[tutorial-slides]: https://slides.com/dvndrsn/graphql-python-tutorial

# Getting started

Before the tutorial begins, please install project prerequisites and perform initial project setup and build.

## Prerequisites

This tutorial requires `git`, `python` version 3.7 or higher, and an code editor such as Visual Studio Code. Node.js is required for running [frontend code samples][tutorial-frontend] in the later part of the tutorial.

### Version control - git

Tutorial code is maintained in a `git` repository.

Refer to [this guide][install-git] for steps to install git on your system.

[install-git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Python 3.7+

The code for this tutorial will work on any Python version >3.6, but using the latest Python 3.7+ is recommended.

Refer to [this guide][install-python] for steps to install Python on your system.

[install-python]: https://docs.python-guide.org/starting/installation/

### Task runner - Invoke

Invoke is a Python task runner library. It can be installed using pip.

```
pip3 install invoke
```

### Node.js 10.15 LTS

Node.js is required to run the frontend code samples from the later part of the tutorial. The [latest LTS version 10.15.3][install-node] is recommended for this tutorial.

[install-node]: https://nodejs.org/en/

### IDE - Visual Studio Code

A code editor with Python support will be very helpful for working through this tutorial.

[Visual Studio Code with Python extension][install-vscode] is highly recommended! It provides autocomplete, typing support and the ability to drill down into defintions for objects.

Be sure to use `Python: Select Interpreter` command to pick the right virtual environment where your dependencies are installed to get the most out of the editor.

[install-vscode]: https://code.visualstudio.com/docs/languages/python

## Initial Setup

Once prerequsites are installed, these instructions can be followed to setup the tutorial code on Linux, OSX and Windows machines.

### Automated script with `invoke`

Setup is scripted using `invoke` python task runner.

Windows users should use pipenv to run `test` and `start` scripts due to terminal issues with `invoke` on the Windows platform.

```
# 0. Install Prerequsites: Python (Target 3.7+), `invoke` and git

# 1. Clone repo
$ git clone https://github.com/dvndrsn/graphql-python-tutorial.git
$ cd graphql-python-tutorial

# 2. Checkout Chapter 1
$ git checkout chapter-1

# 3. Setup dependencies (pipenv, graphene, django, etc.) and fixture data (sqlite) using `invoke`
$ pip3 install invoke
$ invoke setup

# 4. Check setup - lint and test code
$ invoke check  # OR pipenv run test

# 5. Start Django Server
$ invoke start  # OR pipenv run start

# 6. Open GraphiQL - in your web browser
# http://localhost:8000/graphql
```

### Escape hatch for `invoke` script

If `invoke setup` is not working on your machine, you can run the following commands manually to do first time setup, verify that it was successful and start the server.

```
# 3. invoke setup
pip3 install pipenv
pipenv install --dev
                        # (to run inside the virtual environment)
                        # pipenv shell
pipenv run migrate_db   # ./manage.py migrate
pipenv run setup_seed   # ./manage.py loaddata story/fixture.json

# 4. invoke check
pipenv run check_style  # pylint api story cyoa
pipenv run check_types  # mypy api story cyoa
pipenv run test         # ./manage.py test

# 5. invoke start
pipenv run start        # ./manage.py runserver
```

## Frontend Setup

See the [frontend tutorial project][tutorial-frontend] for specific instructions on setting up the demo frontend.

## Important commands

These commands will be useful as you attempt exercises in the tutorial.

### Run server

Some exercises will involve running queries against the GraphQL API. GraphiQL is a tool built into Graphene on our Django server, which provides a user interface to help us run queries for your API.

Run `invoke start` or `pipenv run start`.

Open [`http://localhost:8000/graphql`][graphiql] in your web browser to view the GraphiQL API browser.

Valid queries for the current chapter's schema are defined in `api/queries.graphql`.

[graphiql]: http://localhost:8000/graphql

### Run tests

Some exercises require modification of the GraphQL schema. Unit tests have been prepared for each of these changes so that tests will pass when the changes are implemented correctly.

Run `invoke test` or `pipenv run test`.

# Other Scripts

## List build scripts

All build scripts for this project are defined in Invoke `tasks` module and can be listed using `invoke -l`.

Invoke defers to Pipenv scripts, which can be see in the project `Pipfile`.

## Start a Django shell

The [Django shell][django-shell] is a great sandbox for playing with Django ORM and other Python commmands.

Run `invoke shell` or `pipenv run django_shell` to open the Django shell.

[django-shell]: https://docs.djangoproject.com/en/2.1/ref/django-admin/#shell

## Start web server

Run `invoke start` or `pipenv run start` to start the web server. This allows you to access serveral services on `localhost`.

### GraphiQL

GraphiQL is a great sandbox for playing with GraphQL queries.

Open [`http://localhost:8000/graphql`][graphiql] in your web browser to view the GraphiQL API browser.

[graphiql]: http://localhost:8000/graphql

### Django Admin Panel

Run `invoke setup.superuser` `pipenv run setup_superuser` and set your username and password.

The Django admin panel can be used to add new data to our models. You shouldn't need to do this, but feel free to have fun with it!

When the server is running, open [`localhost:8000/admin`][django-admin] in your browser to view the admin panel.

[django-admin]: http://localhost:8000/admin

## Check Code style - PyLint

Run `invoke lint` or `invoke check.style` or `pipenv run check_style` to verify coding style.

This is not needed for completion of the execerises, but is used to verify the tutorial code has consistent style.

[reference-pylint]: https://pylint.readthedocs.io/en/stable/user_guide/output.html

## Check Type Annotations - MyPy

Run `invoke lint` or `invoke check.types` or `pipenv run check_types` to verify static type annotations.

This is not needed for completion of the execerises, but is used to verify that the tutorial code has consistent and correct type annotations.
