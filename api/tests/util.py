from django.test import RequestFactory


def request_with_loaders():
    factory = RequestFactory()
    request = factory.post('graphql')
    return request


def connection_to_list(connection):
    return [dict(edge['node']) for edge in connection['edges']]
