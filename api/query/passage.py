from typing import Any, Iterable, Optional

import graphene

from story.models import Passage, Story, Character, Choice


class PassageType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()
    description = graphene.String()
    is_ending = graphene.Boolean()

    story = graphene.Field('api.query.story.StoryType')
    character = graphene.Field('api.query.character.CharacterType')
    all_choices = graphene.List('api.query.choice.ChoiceType')

    @staticmethod
    def resolve_story(root: Passage, info: graphene.ResolveInfo) -> Story:
        return root.story

    @staticmethod
    def resolve_character(root: Passage, info: graphene.ResolveInfo) -> Optional[Character]:
        return root.pov_character

    @staticmethod
    def resolve_all_choices(root: Passage, info: graphene.ResolveInfo) -> Iterable[Choice]:
        return root.to_choices.all() # type: ignore

    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Passage)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Optional[Passage]:
        try:
            key = int(id_)
            return Passage.objects.get(pk=key)
        except Passage.DoesNotExist:
            return None


class PassageConnection(graphene.Connection):

    class Meta:
        node = PassageType


class Query(graphene.ObjectType):
    node = graphene.Node.Field()
