from collections import namedtuple

import graphql_relay


def to_global_id(type_, id_):
    type_name = str(type_)
    return graphql_relay.to_global_id(type_name, id_)


GlobalID = namedtuple('GlobalID', ('type_name', 'type_id'))


def from_global_id(global_id):
    type_name, type_id = graphql_relay.from_global_id(global_id)
    return GlobalID(type_name, int(type_id))
