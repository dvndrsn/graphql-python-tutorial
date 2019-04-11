from typing import Any, Iterable, Optional, List

import graphene
from promise import Promise

from story import models


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = models.Author.DISPLAY_FIRST_LAST
    LAST_FIRST = models.Author.DISPLAY_LAST_FIRST


class AuthorType(graphene.ObjectType):

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

    stories = graphene.ConnectionField('api.query.story.StoryConnection')

    @staticmethod
    def resolve_full_name(root: models.Author, info: graphene.ResolveInfo, display: str) -> str:
        return root.full_name(display)

    @staticmethod
    def resolve_stories(root: models.Author, info: graphene.ResolveInfo, **kwargs
                       ) -> Promise[List[models.Story]]:
        return info.context.loaders.stories_from_author.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Author)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str
                ) -> Promise[Optional[models.Author]]:
        key = int(decoded_id)
        return info.context.loaders.author.load(key)


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
