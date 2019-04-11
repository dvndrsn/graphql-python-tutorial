from typing import Any, Optional

import graphene

from story.models import Choice, Passage


class ChoiceType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    description = graphene.String()
    is_main_story = graphene.Boolean()

    from_passage = graphene.Field('api.query.passage.PassageType')
    to_passage = graphene.Field('api.query.passage.PassageType')

    @staticmethod
    def resolve_from_passage(root: Choice, info: graphene.ResolveInfo, **kwargs) -> Passage:
        return root.from_passage

    @staticmethod
    def resolve_to_passage(root: Choice, info: graphene.ResolveInfo, **kwargs) -> Passage:
        return root.to_passage

    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Choice)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Optional[Choice]:
        try:
            key = int(id_)
            return Choice.objects.get(pk=key)
        except Choice.DoesNotExist:
            return None


class ChoiceConnection(graphene.Connection):

    class Meta:
        node = ChoiceType


class Query(graphene.ObjectType):
    node = graphene.Node.Field()
