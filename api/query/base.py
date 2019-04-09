from .author import Query as AuthorQuery
from .story import Query as StoryQuery


class Query(
        AuthorQuery,
        StoryQuery,
):
    pass
