from typing import Any, Iterable, Optional

import graphene

from story import models


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = models.Author.DISPLAY_FIRST_LAST
    LAST_FIRST = models.Author.DISPLAY_LAST_FIRST


class AuthorType(graphene.ObjectType):
    # Exercise 4b.
    # Add AuthorType.stories and Stories.author fields.
    # - run `invoke test` to verify the changes using a test case
    # - run `invoke start` to run queries against `localhost:8000/graphql`
    # - sample queries available in `api/queries.graphql`

    # Our ORM object, `models.Author` has attributes to resolve these fields.
    # - a one to many field - `stories`

    # Remember:
    # - graphene.Field can take any GraphQL type (such as ObjectType). It can also take a module
    #     string like 'api.query.passage.PassageType' to help avoid circular imports.
    # - REFERENCE.md may be helpful to brush up on Django ORM as well!
    # - keyword arguments need to be accepted for ConnectionField resolvers even tho graphene does
    #     the heavy lifting

    # AuthorType schema changes"
    # - add a connection field `stories` that points a paginated connection of StoryType
    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()
    twitter_account = graphene.String()
    full_name = graphene.String(
        args={
            'display': graphene.Argument(
                AuthorDisplayNameEnum,
                required=True,
                default_value=AuthorDisplayNameEnum.FIRST_LAST,
                description='Display format to use for Full Name of Author - default FIRST_LAST.'
            )
        }
    )

    # AuthorType resolver changes:
    # - leverage one-to-many connection from author to stories for `stories` field
    @staticmethod
    def resolve_full_name(root: models.Author, info: graphene.ResolveInfo, display: str) -> str:
        return root.full_name(display)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Author)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Optional[models.Author]:
        try:
            key = int(id_)
            return models.Author.objects.get(pk=key)
        except models.Author.DoesNotExist:
            return None


class AuthorConnection(graphene.Connection):

    class Meta:
        node = AuthorType


class Query(graphene.ObjectType):

    node = graphene.Node.Field()
    authors = graphene.ConnectionField(AuthorConnection)

    @staticmethod
    def resolve_authors(root: None, info: graphene.ResolveInfo, **kwargs
                       ) -> Iterable[models.Author]:
        return models.Author.objects.all()
