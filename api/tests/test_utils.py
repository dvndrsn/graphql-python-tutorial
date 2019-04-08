from django.test import TestCase
import graphene

from api.utils import to_global_id, from_global_id, GlobalID


class TestGlobalId(TestCase):

    def test_to_global_id__can_be_decoded_from_type_name(self):
        class TypeWithGlobalIDAndName(graphene.ObjectType):
            class Meta:
                interfaces = (graphene.Node, )
                name = 'WithGlobalID'

        encoded = to_global_id(TypeWithGlobalIDAndName, 2)

        decoded = from_global_id(encoded)
        self.assertEqual(decoded, GlobalID('WithGlobalID', 2))

    def test_to_global_id__can_be_decoded_from_default_name(self):
        class TypeWithGlobalIDWithoutName(graphene.ObjectType):
            class Meta:
                interfaces = (graphene.Node, )

        encoded = to_global_id(TypeWithGlobalIDWithoutName, 3)

        decoded = from_global_id(encoded)
        self.assertEqual(decoded, GlobalID('TypeWithGlobalIDWithoutName', 3))
