from typing import Any, List, Optional

import graphene
from promise import Promise

from story.models import Character, Passage


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()
    in_passages = graphene.ConnectionField('api.query.passage.PassageConnection')

    @staticmethod
    def resolve_in_passages(root: Character, info: graphene.ResolveInfo,
                            **kwargs) -> Promise[List[Passage]]:
        return info.context.loaders.passage_from_pov_character.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Character)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Character]]:
        key = int(decoded_id)
        return info.context.loaders.character.load(key)



class Query(graphene.ObjectType):
    node = graphene.Node.Field()
