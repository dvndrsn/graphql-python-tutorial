from django.test import TestCase
import graphene

from api.query.character import Query, CharacterType
from api.query.passage import PassageType
from api.tests.util import connection_to_list, request_with_loaders
from api.utils import to_global_id
from story.factories import CharacterFactory, PassageFactory


class TestCharacterNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query, types=(CharacterType,))
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getCharacterNode($id: ID!) {
            character: node(id: $id) {
                ... on CharacterType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_character_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(CharacterType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data, {'character': None})

    def test_character_node_query__returns_model_fields(self):
        CharacterFactory.create(id=7, name='Lil Bobby')
        query_string = self.build_query_with_fields('id', 'name')
        variables = {'id': to_global_id(CharacterType, 7)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data['character'], {
            'id': to_global_id(CharacterType, 7),
            'name': 'Lil Bobby'
        })

    def test_character_node_query__returns_related_passages(self):
        character = CharacterFactory(id=6)
        PassageFactory.create(id=4, pov_character=character)
        PassageFactory.create(id=5, pov_character=character)
        query_string = self.build_query_with_fields(
            'id',
            'inPassages { edges { node { id } } }',
        )
        variables = {'id': to_global_id(CharacterType, 6)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertEqual(connection_to_list(result.data['character']['inPassages']), [
            {'id': to_global_id(PassageType, 4)},
            {'id': to_global_id(PassageType, 5)},
        ])
