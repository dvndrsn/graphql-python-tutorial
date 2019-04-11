from typing import Any, Iterable, Optional

import graphene

from story.models import Character, Passage


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()
    in_passages = graphene.ConnectionField('api.query.passage.PassageConnection')

    @staticmethod
    def resolve_in_passages(root: Character, info: graphene.ResolveInfo,
                            **kwargs) -> Iterable[Passage]:
        return root.in_passages.all() # type: ignore

    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Character)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Optional[Character]:
        try:
            key = int(id_)
            return Character.objects.get(pk=key)
        except Character.DoesNotExist:
            return None



class Query(graphene.ObjectType):
    node = graphene.Node.Field()
