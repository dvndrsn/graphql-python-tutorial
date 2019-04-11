from django.utils.functional import cached_property

from .util import batch_load_primary_key, DataLoader


class AuthorLoaders:

    @cached_property
    def author(self):
        author_load_fn = batch_load_primary_key('story', 'Author')
        return DataLoader(author_load_fn)
