from .author import Query as AuthorQuery
from .character import Query as CharacterQuery
from .choice import Query as ChoiceQuery
from .passage import Query as PassageQuery
from .story import Query as StoryQuery


class Query(
        AuthorQuery,
        CharacterQuery,
        ChoiceQuery,
        PassageQuery,
        StoryQuery,
):
    pass
