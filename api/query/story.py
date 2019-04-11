from typing import Any, Iterable, Optional

import graphene

from story import models
from api.query.author import AuthorDisplayNameEnum


class StoryType(graphene.ObjectType):
    # Exercise 4b.
    # Add AuthorType.stories and Stories.author fields.
    # - run `invoke test` to verify the changes using a test case
    # - run `invoke start` to run queries against `localhost:8000/graphql`
    # - sample queries available in `api/queries.graphql`

    # Our ORM object, `models.Story` has attributes to resolve these fields.
    # - a many to one field - `author`

    # Remember:
    # - graphene.Field can take any GraphQL type (such as ObjectType). It can also take a module
    #     string like 'api.query.passage.PassageType' to help avoid circular imports.
    # - REFERENCE.md may be helpful to brush up on Django ORM as well!

    # AuthorType schema changes"
    # - add a field `author` that points a single AuthorType
    class Meta:
        interfaces = (graphene.Node, )

    title = graphene.String()
    subtitle = graphene.String()
    description = graphene.String()
    published_year = graphene.String()
    author_name = graphene.String(
        args={
            'display': graphene.Argument(
                AuthorDisplayNameEnum,
                default_value=AuthorDisplayNameEnum.FIRST_LAST,
                description='Display format to use for Full Name of Author - default FIRST_LAST.'
            )
        }
    )

    # StoryType resolver changes:
    # - leverage many-to-one connection from stories to author for `author` field
    @staticmethod
    def resolve_author_name(root: models.Story, info: graphene.ResolveInfo, display: str) -> str:
        return root.author.full_name(display)

    @staticmethod
    def resolve_published_year(root: models.Story, info: graphene.ResolveInfo) -> str:
        return str(root.published_date.year)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Story)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Optional[models.Story]:
        try:
            key = int(id_)
            return models.Story.objects.get(pk=key)
        except models.Story.DoesNotExist:
            return None


class StoryConnection(graphene.Connection):

    class Meta:
        node = StoryType


class Query(graphene.ObjectType):
    stories = graphene.ConnectionField(StoryConnection)
    node = graphene.Node.Field()

    @staticmethod
    def resolve_stories(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[models.Story]:
        return models.Story.objects.all()
