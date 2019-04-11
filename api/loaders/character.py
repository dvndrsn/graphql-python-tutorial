from django.utils.functional import cached_property

from .util import batch_load_primary_key, DataLoader


class CharacterLoaders:

    @cached_property
    def character(self) -> DataLoader:
        character_load_fn = batch_load_primary_key('story', 'Character')
        return DataLoader(character_load_fn)
