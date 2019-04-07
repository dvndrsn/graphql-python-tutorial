# Reference

Reviewing this reference will provide some background on the dependencies used in this tutorial. Refer to this section as a quick refresher before the tutorial or in case you get stuck during an exercise.

## Version Control - git

Branches are used for each chapter of our tutorial.

You should be comfortable switching branches with `git checkout` and ensuring your working tree is clean by either using `git commit`, `git stash` or `git reset`. You can safely check out each branch and commit to it without affecting future chapters' work.

A knowledge of basic git commands like [`checkout`][git-checkout-reference] and [`stash`][git-stash-reference] should get you through the tutorial, but [this whole guide from Atlassian][git-save-reference] is very friendly and helpful.

[git-checkout-reference]: https://www.atlassian.com/git/tutorials/using-branches/git-checkout
[git-stash-reference]: https://www.atlassian.com/git/tutorials/saving-changes/git-stash
[git-save-refence]: https://www.atlassian.com/git/tutorials/saving-changes

```
# checkout a chapter branch
$ git checkout chapter-1

# save work in progress
$ git add .
$ git commit -m 'my cool commit message here'

# stash work in progress (temporary save)
$ git stash
# list, apply, pop are other useful git stash commands
```

If you get into a state where things seem too hard to correct, some more advanced commands can help:

```
# get rid of work in progress
$ git reset --hard

# git rid of work in progress and reset chapter branch the original state
$ git reset --hard origin/<branch-name>
```

[This article from GitLab][git-undo] is a great overview of strategies to undo local changes if you get stuck during the tutorial.

[git-undo]: https://docs.gitlab.com/ee/topics/git/numerous_undo_possibilities_in_git/#undo-local-changes

## Virtual Environment - Pipenv

Pipenv is a tool used to manage our Python virtual environment for this project. Most of our build commands use `pipenv run` to execute in the context of the active virtual environment.

```
# install dependencies
$ pipenv install

# "activate" virtual environment in terminal shell
$ pipenv shell

# "deactive" virtual environment in terminal shell
(graphql-python-tutorial) $ exit
```

[This article from Python Guide][pipenv-reference] gives a great overview of the benefits of Pipenv and different strategies for using virtual environments with Python.

[pipenv-reference]: https://docs.python-guide.org/dev/virtualenvs/

## Python + Standard Libraries

This tutorial was written using [Python 3.7+][python-reference]. Being familiar with idiomatic python, classes and inheritance, staticmethod vs instance method, packages and modules and the `datetime.date` object will be helpful for understanding the tutorial content and exercises.

[python-reference]: https://docs.python.org/3/

## Testing - UnitTest

You won't need to _write_ any tests during this tutorial, but being able to read the output of a failing test and read some test code, it will be very helpful! Take a brief moment to review [the Python standard library documentation for `unittest`][reference-unittest].

[reference-unittest]: http://docs.python.org/3/library/unittest.html

The tests written for this tutorial follow the pattern Arrange, Act, Assert, each separated by a line break.

- Arrange: Setup test data needed to run code we're testing
- Act: Call the function that we're testing and get results. In this case, we're almost executing a query against our schema.
- Assert: Make assertions against the results. Most of our tests verify that the query had no errors and the data matches our expected values.

Here's an example of a failing test output. Useful information that this failing test gives us:

- Failing test name and class. We can open that class to take a closer look: `test_story_node_query__returns_model_fields (api.tests.query.test_story.TestStoriesQuery)`
- Traceback for where the error happened. We can look at the specific line where the test failed (`Traceback ...line 70, in...`).
- Error and Difference between actual/expected results. In this case, our own assertion threw the error and the diff. The diff is that expected results have '2019' for 'publishedYear' but actual is `None`.
- Sometimes an additional message is added to an assertion by the test writer to help debug problems. In this case, we output the GraphQL query for reference.

```
  $  invoke test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..F..
======================================================================
FAIL: test_story_node_query__returns_model_fields (api.tests.query.test_story.TestStoriesQuery)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/daveanderson/projects/dvndrsn/graphql-python-tutorial/api/tests/query/test_story.py", line 70, in test_story_node_query__returns_model_fields
    }, msg=f'Query data in result does not match for: {query_string}')
AssertionError: {'id'[55 chars]QL', 'description': 'A big adventure', 'publishedYear': None} != {'id'[55 chars]QL', 'description': 'A big adventure', 'publishedYear': '2019'}
  {'description': 'A big adventure',
   'id': '2',
-  'publishedYear': None,
?                   ^^^^

+  'publishedYear': '2019',
?                   ^^^^^^

   'subtitle': 'Hello GraphQL',
   'title': 'Hello world'} : Query data in result does not match for:
        query getStories {
            stories {
                id title subtitle description publishedYear
            }
        }


----------------------------------------------------------------------
Ran 5 tests in 0.012s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

## Type Annotations - MyPy

You don't need to _write_ any type annotations during this tutorial, but being able to read them in code will help make some of the examples in this tutorial more clear.

Type annotations allow you to indicate a type of data expected for each argument and return value of a function. This is leveraged by MyPy to provide static type checks and can also be used by IDE to provide better autocomplete suggestions (VSCode Python extension does a great job of this).

The sytax is pretty straightforward! Each argument is annotated with a type after a colon like `display: str` for a string argument `display` and the type for the return value is annotated with a skinny arrow followed by the type like `-> str` for a function returning a string.

```
    @staticmethod
    def resolve_author_name(
        # argument: type
        root: models.Story,
        info: graphene.ResolveInfo,
        display: str,
    ) -> str:
    # -> return_type
        return root.author.full_name(display)
```

Refer to this [MyPy cheat sheet][mypy-reference] for more detailed information.

[mypy-reference]: https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html

## Django - ORM Web Framework - Django

The Django web framework provides the backbone for our API in this tutorial, processing web requests, managing migrations of our models in the database and providing Object Relational Mapping (ORM) to interact with the database.

In the exercises, you will need to write some basic [ORM queries][django-reference] using Django models to resolve data for our API.

Here a few useful methods for reading records from the database.

```
# Select a single author
author = Author.objects.get(pk=2)

# Quereyset - Select all Authors
all_authors = Author.objects.all()

# Queryset - Select only stories with matching criteria
stories = Story.objects.filter(author__in=author)
first_story = stories[0]

# Many-to-one - access model across foreign key
first_story.author

# One-to-many - access model across foreign key
author.stories.all()

```

[django-reference]: https://docs.djangoproject.com/en/2.1/ref/models/querysets/

## RESTful Web Services

We'll discuss and compare RESTful web servies to GraphQL during this tutorial.

If you want to brush up on REST, [Smashing Magazine has a nice breezy article][rest-overview-reference] with a broad overview of REST. [The Google API Design Guide][api-design-reference] is a much deeper dive and covers some of the ideas that apply to GraphQL as well. We'll briefly cover this in the tutorial though!

[rest-overview-reference]: https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/
[api-design-reference]: https://cloud.google.com/apis/design/resource_names

## GraphQL Web Services

The meat of the tutorial will cover GraphQL very thoroughly. We'll be using Graphene as our python graphql implementation. Feel free to take a look at the [Graphene docs][graphene-reference].

If you want a sneak peak of GraphQL (and the interative query builder GraphiQL), I'd suggest taking a look at a public API, like GitHub. GitHub's V4 GraphQL API is a great example of a Relay-compliant GraphQL API, with rich domain. Just login using your github credentials to explore!

https://developer.github.com/v4/explorer/

Here's a sample query:

```
query myGithubComments {
  viewer {
    login
    bio
    issueComments(last: 10) {
      edges {
        node {
          createdAt
          id
          body
          url
        }
      }
    }
  }
}
```

[graphene-reference]: https://docs.graphene-python.org/en/latest/

## JavaScript + ES6 + React

We'll go through a sample React application using Apollo client during the tutorial. Being aware of basic concepts like `JSX` in React and `Arrow functions` in ES6 will help make the syntax in examples more clear, but we won't be writing any JavaScript or React, so don't sweat it too much!
