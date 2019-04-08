from typing import Iterable

import graphene

from story.models import Story, Author


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = Author.DISPLAY_FIRST_LAST
    LAST_FIRST = Author.DISPLAY_LAST_FIRST


class StoryType(graphene.ObjectType):

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

    @staticmethod
    def resolve_author_name(root: Story, info: graphene.ResolveInfo, display: str) -> str:
        return root.author.full_name(display)


class Query(graphene.ObjectType):
    stories = graphene.List(StoryType)

    @staticmethod
    def resolve_stories(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Story]:
        return Story.objects.all()
