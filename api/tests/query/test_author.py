from django.test import TestCase
import graphene

from api.query.author import Query, AuthorType
from api.tests.util import connection_to_list, request_with_loaders
from api.utils import to_global_id
from story.factories import AuthorFactory


class TestAuthorConnection(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getAuthors {
            authors {
                edges {
                    node {
                        %s
                    }
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_authors_query__returns_list_of_stories(self):
        AuthorFactory.create(id=2)
        AuthorFactory.create(id=5)
        query_string = self.build_query_with_fields('id')

        result = self.schema.execute(query_string, context=self.request)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertListEqual(connection_to_list(result.data['authors']), [
            {'id': to_global_id(AuthorType, 2)},
            {'id': to_global_id(AuthorType, 5)},
        ], msg=f'Query data in result does not match for: {query_string}')


class TestAuthorNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query, types=(AuthorType,))
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getAuthorNode($id: ID!) {
            author: node(id: $id) {
                ... on AuthorType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_author_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(AuthorType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertDictEqual(result.data, {'author': None},
                             msg=f'Query data in result does not match for: {query_string}')

    def test_author_node_query__returns_model_fields(self):
        AuthorFactory.create(
            id=3,
            first_name='Buddy',
            last_name='Holly',
            twitter_account='@buddy',
        )
        query_string = self.build_query_with_fields(
            'id',
            'firstName',
            'lastName',
            'twitterAccount',
        )
        variables = {'id': to_global_id(AuthorType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertDictEqual(dict(result.data['author']), {
            'id': to_global_id(AuthorType, 3),
            'firstName': 'Buddy',
            'lastName': 'Holly',
            'twitterAccount': '@buddy',
        }, msg=f'Query data in result does not match for: {query_string}')

    def test_author_full_name_field__display_last_first(self):
        AuthorFactory.create(
            id=3,
            first_name='Buddy',
            last_name='Holly',
        )
        query_string = self.build_query_with_fields(
            'id',
            'fullName (display: LAST_FIRST)',
        )
        variables = {'id': to_global_id(AuthorType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertEqual(result.data['author']['fullName'], 'Holly, Buddy',
                         msg=f'Query data in result does not match for: {query_string}')

    def test_author_full_name_field__display_first_last(self):
        AuthorFactory.create(
            id=3,
            first_name='Buddy',
            last_name='Holly',
        )
        query_string = self.build_query_with_fields(
            'id',
            'fullName (display: FIRST_LAST)',
        )
        variables = {'id': to_global_id(AuthorType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors, msg=f'Query errors prevented execution for {query_string}')
        self.assertEqual(result.data['author']['fullName'], 'Buddy Holly',
                         msg=f'Query data in result does not match for: {query_string}')
