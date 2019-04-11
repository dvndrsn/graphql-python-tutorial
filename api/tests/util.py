from django.test import RequestFactory

from api.loaders.base import Loaders


def request_with_loaders():
    factory = RequestFactory()
    request = factory.post('graphql')
    request.loaders = Loaders()
    return request


def connection_to_list(connection):
    return [dict(edge['node']) for edge in connection['edges']]
