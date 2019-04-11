from .author import AuthorLoaders
from .story import StoryLoaders
from .passage import PassageLoaders
from .choice import ChoiceLoaders
from .character import CharacterLoaders


class Loaders(
        AuthorLoaders,
        StoryLoaders,
        PassageLoaders,
        ChoiceLoaders,
        CharacterLoaders,
):
    pass
