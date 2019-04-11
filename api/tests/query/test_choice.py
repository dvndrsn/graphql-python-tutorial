from django.test import TestCase
import graphene

from api.query.choice import ChoiceType, Query
from api.query.passage import PassageType
from api.tests.util import request_with_loaders
from api.utils import to_global_id
from story.factories import PassageFactory, ChoiceFactory


class TestAuthorNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query, types=(ChoiceType,))
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getChoiceNode($id: ID!) {
            choice: node(id: $id) {
                ... on ChoiceType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_choice_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(ChoiceType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors)
        self.assertDictEqual(result.data, {'choice': None})

    def test_choice_node_query__returns_model_fields(self):
        ChoiceFactory.create(
            id=3,
            description='Do the right thing',
            is_main_story=True
        )
        query_string = self.build_query_with_fields(
            'id',
            'description',
            'isMainStory',
        )
        variables = {'id': to_global_id(ChoiceType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors)
        self.assertDictEqual(result.data['choice'], {
            'id': to_global_id(ChoiceType, 3),
            'description': 'Do the right thing',
            'isMainStory': True,
        })

    def test_choice_node_query__returns_related_from_passage(self):
        passage = PassageFactory(id=5)
        ChoiceFactory.create(id=3, from_passage=passage)
        query_string = self.build_query_with_fields(
            'id',
            'fromPassage { id }',
        )
        variables = {'id': to_global_id(ChoiceType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors)
        self.assertDictEqual(result.data['choice']['fromPassage'], {
            'id': to_global_id(PassageType, 5)
        })

    def test_choice_node_query__returns_related_to_passage(self):
        passage = PassageFactory(id=2)
        ChoiceFactory.create(id=3, to_passage=passage)
        query_string = self.build_query_with_fields(
            'id',
            'toPassage { id }',
        )
        variables = {'id': to_global_id(ChoiceType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertIsNone(result.errors)
        self.assertDictEqual(result.data['choice']['toPassage'], {
            'id': to_global_id(PassageType, 2)
        })
