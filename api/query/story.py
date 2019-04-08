from typing import Iterable

import graphene

from story import models


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = models.Author.DISPLAY_FIRST_LAST
    LAST_FIRST = models.Author.DISPLAY_LAST_FIRST


class StoryType(graphene.ObjectType):
    # Exercise 2:
    # Add publishedYear and description fields to StoryType in our GraphQL schema.
    # Graphene needs field schema definition and a resolver function for each field.
    # - run `invoke test` to verify the changes using a test case
    # - run `invoke start` to run queries against `localhost:8000/graphql`
    # - sample queries available in `api/queries.graphql`

    # Our Django Story model has the following attributes that we can use to resolve our new fields:
    # - description - string
    # - published_date - datetime.date
    #     (https://docs.python.org/3/library/datetime.html#available-types)
    #
    # Resolving `description` field may be easier than resolving just the year of the
    # Story `published_date`!

    # This is our schema defintion.
    # We tell Graphene what the field name and type should be:
    # - <field_name> = graphene.<ScalarType>()
    # - Graphene automatically camelCases our snake_cased field names for the GraphQL schema
    id = graphene.ID()
    title = graphene.String()
    subtitle = graphene.String()
    author_name = graphene.String(
        args={
            'display': graphene.Argument(
                AuthorDisplayNameEnum,
                default_value=AuthorDisplayNameEnum.FIRST_LAST,
                description='Display format to use for Full Name of Author - default FIRST_LAST.'
            )
        }
    )

    # These are our resolver functions.
    # - def resolve_<field_name>(root, info): return root.<data_to_resolve>
    # - root in this case is our Django Story model, resolved from Query.resolve_stories.
    # - title and subtile fields are resolved implicitly since the field matches the attribute on
    #     root (the Story model)
    @staticmethod
    def resolve_author_name(root: models.Story, info: graphene.ResolveInfo, display: str) -> str:
        return root.author.full_name(display)


class Query(graphene.ObjectType):
    stories = graphene.List(StoryType)

    @staticmethod
    def resolve_stories(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[models.Story]:
        return models.Story.objects.all()
