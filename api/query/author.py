from typing import Any, List, Iterable, Optional # pylint: disable=unused-import

import graphene

from story import models


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = models.Author.DISPLAY_FIRST_LAST
    LAST_FIRST = models.Author.DISPLAY_LAST_FIRST


class AuthorType(graphene.ObjectType):
    # Exercise 4!
    # Let's evolve the schema to include an AuthorType and AuthorConnection!
    # - run `invoke test` to verify the changes using a test case
    # - run `invoke start` to run queries against `localhost:8000/graphql`
    # - sample queries available in `api/queries.graphql`

    # The `models.Author` object has the following attributes to use to resolve our new fields:
    # - id - ID
    # - String - first_name, last_name, twitter_account
    # - function for formatting names - full_name(display) -> str

    # Remember:
    # - Refer to `api/query/story.py` for examples of similar implementation.
    # - REFERENCE.md may be helpful to brush up on Django ORM as well!
    # - Graphene auto-camelCases fields from our Python code!

    # AuthorType schema changes:
    # - Ensure AuthorType has the following String fields in the GraphQL schema:
    #   - id, firstName, lastName, twitterAccount, fullName
    # - AuthorType should implement the Node Interface (as StoryType does)
    dummy = graphene.String(description='Enter your stuff here')

    # AuthorType resovler changes:
    # - AuthorType.fullName field should have similar implementation as StoryType.fullName
    # - AuthorType should implement `get_node` to fetch a single Author from the ORM
    # - AuthorType should implement `is_type_of` to disambiguate inline fragments in our queries


# Add a new type:
# - Implement AuthorConnection with AuthorType as node

class Query(graphene.ObjectType):
    # Query schema changes:
    # - Add Query.authors connection field to paginate over authors
    node = graphene.Node.Field()

    # Query resolver changes:
    # - Add a resolver for authors
