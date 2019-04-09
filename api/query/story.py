from typing import Any, Iterable, Optional

import graphene

from story import models


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = models.Author.DISPLAY_FIRST_LAST
    LAST_FIRST = models.Author.DISPLAY_LAST_FIRST


class StoryType(graphene.ObjectType):

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
