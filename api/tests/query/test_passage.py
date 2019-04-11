from django.test import TestCase
import graphene

from api.query.character import CharacterType
from api.query.choice import ChoiceType
from api.query.passage import Query, PassageType
from api.query.story import StoryType
from api.tests.util import request_with_loaders
from api.utils import to_global_id
from story.factories import StoryFactory, PassageFactory, CharacterFactory, ChoiceFactory


class TestAuthorNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query, types=(PassageType,))
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getPassageNode($id: ID!) {
            passage: node(id: $id) {
                ... on PassageType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_passage_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(PassageType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data, {'passage': None})

    def test_passage_node_query__returns_model_fields(self):
        PassageFactory.create(
            id=7,
            name='Passage 2',
            description='Something good happens',
            is_ending=True,
        )
        query_string = self.build_query_with_fields(
            'id',
            'name',
            'description',
            'isEnding',
        )
        variables = {'id': to_global_id(PassageType, 7)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data['passage'], {
            'id': to_global_id(PassageType, 7),
            'name': 'Passage 2',
            'description': 'Something good happens',
            'isEnding': True,

        })

    def test_passage_node_query__returns_related_story(self):
        story = StoryFactory.create(id=2)
        PassageFactory(id=5, story=story)
        query_string = self.build_query_with_fields(
            'id',
            'story { id }',
        )
        variables = {'id': to_global_id(PassageType, 5)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data['passage']['story'], {
            'id': to_global_id(StoryType, 2)
        })

    def test_passage_node_query__returns_related_character(self):
        character = CharacterFactory.create(id=4)
        PassageFactory(id=5, pov_character=character)
        query_string = self.build_query_with_fields(
            'id',
            'character { id }',
        )
        variables = {'id': to_global_id(PassageType, 5)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data['passage']['character'], {
            'id': to_global_id(CharacterType, 4)
        })

    def test_passage_node_query__returns_list_of_choices(self):
        passage = PassageFactory(id=2)
        ChoiceFactory(id=3, from_passage=passage)
        ChoiceFactory(id=1, from_passage=passage)
        query_string = self.build_query_with_fields(
            'id',
            'allChoices { id }',
        )
        variables = {'id': to_global_id(PassageType, 2)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data['passage']['allChoices'], [
            {'id': to_global_id(ChoiceType, 1)},
            {'id': to_global_id(ChoiceType, 3)},
        ])
