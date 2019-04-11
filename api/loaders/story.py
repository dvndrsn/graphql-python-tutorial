from django.utils.functional import cached_property

from .util import batch_load_primary_key, batch_load_foreign_key, DataLoader


class StoryLoaders:

    @cached_property
    def story(self) -> DataLoader:
        story_load_fn = batch_load_primary_key('story', 'Story')
        return DataLoader(story_load_fn)

    @cached_property
    def stories_from_author(self) -> DataLoader:
        stories_from_author_load_fn = batch_load_foreign_key('story', 'Story', 'author')
        return DataLoader(stories_from_author_load_fn)
