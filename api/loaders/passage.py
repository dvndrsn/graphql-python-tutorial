from django.utils.functional import cached_property

from .util import batch_load_foreign_key, batch_load_primary_key, DataLoader


class PassageLoaders:

    @cached_property
    def passage(self) -> DataLoader:
        passage_load_fn = batch_load_primary_key('story', 'Passage')
        return DataLoader(passage_load_fn)

    @cached_property
    def passage_from_story(self) -> DataLoader:
        passage_from_story_load_fn = batch_load_foreign_key('story', 'Passage', 'story')
        return DataLoader(passage_from_story_load_fn)

    @cached_property
    def passage_from_pov_character(self) -> DataLoader:
        passage_from_pov_character_fn = batch_load_foreign_key(
            'story',
            'Passage',
            'pov_character',
        )
        return DataLoader(passage_from_pov_character_fn)
