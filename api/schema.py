import graphene

from .query import Query
from .mutation import Mutation


SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
