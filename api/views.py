from graphene_django.views import GraphQLView as BaseGraphQLView

from .loaders import Loaders


class GraphQLView(BaseGraphQLView):
    def get_context(self, request):
        request.loaders = getattr(request, 'loaders', Loaders())
        return request
