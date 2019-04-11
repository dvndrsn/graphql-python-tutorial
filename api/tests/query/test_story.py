from django.test import TestCase
import graphene

from api.query.story import Query, StoryType
from api.query.author import AuthorType
from api.tests.util import connection_to_list, request_with_loaders
from api.utils import to_global_id
from story.factories import StoryFactory, AuthorFactory


class TestStoriesQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getStories {
            stories {
                edges {
                    node {
                        %s
                    }
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_stories_query__returns_list_of_stories(self):
        StoryFactory.create(id=2)
        StoryFactory.create(id=5)
        query_string = self.build_query_with_fields('id')

        result = self.schema.execute(query_string, context=self.request)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertListEqual(connection_to_list(result.data['stories']), [
            {'id': to_global_id(StoryType, 2)},
            {'id': to_global_id(StoryType, 5)},
        ], msg=f'Query data in result does not match for: {query_string}')


class TestStoryNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getStoryNode($id: ID!) {
            story: node(id: $id) {
                ... on StoryType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_story_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(StoryType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertDictEqual(result.data, {'story': None},
                             msg=f'Query data in result does not match for: {query_string}')

    def test_story_node_query__returns_model_fields(self):
        StoryFactory.create(
            id=2,
            title='Hello world',
            subtitle='Hello GraphQL',
            description='A big adventure',
            published_date='2019-05-04',
        )
        query_string = self.build_query_with_fields(
            'id',
            'title',
            'subtitle',
            'description',
            'publishedYear',
        )
        variables = {'id': to_global_id(StoryType, 2)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertDictEqual(dict(result.data['story']), {
            'id': to_global_id(StoryType, 2),
            'title': 'Hello world',
            'subtitle': 'Hello GraphQL',
            'description': 'A big adventure',
            'publishedYear': '2019',
        }, msg=f'Query data in result does not match for: {query_string}')

    def test_story_node_query__returns_related_author(self):
        StoryFactory.create(
            id=2,
            author=AuthorFactory(id=5)
        )
        query_string = self.build_query_with_fields(
            'id',
            'author { id }',
        )
        variables = {'id': to_global_id(StoryType, 2)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertDictEqual(dict(result.data['story']['author']), {
            'id': to_global_id(AuthorType, 5),
        }, msg=f'Query data in result does not match for: {query_string}')
