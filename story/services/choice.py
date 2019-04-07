from rest_framework import serializers

from story.models import Choice, Passage


class ChoiceService(serializers.Serializer):
    description = serializers.CharField()
    is_main_story = serializers.BooleanField()
    from_passage_id = serializers.IntegerField()
    to_passage_id = serializers.IntegerField()

    to_passage = None
    from_passage = None

    def validate_from_passage_id(self, from_passage_id: int) -> int:
        try:
            self.from_passage = Passage.objects.get(pk=from_passage_id)
            return from_passage_id
        except Passage.DoesNotExist:
            raise serializers.ValidationError('From Passage does not exist')

    def validate_to_passage_id(self, to_passage_id: int) -> int:
        try:
            self.to_passage = Passage.objects.get(pk=to_passage_id)
            return to_passage_id
        except Passage.DoesNotExist:
            raise serializers.ValidationError('To Passage does not exist')

    def validate(self, attrs: dict) -> dict:
        if self.to_passage and self.from_passage and \
            not self.to_passage.story_id == self.from_passage.story_id:
            raise serializers.ValidationError('Passages must be from the same Story')
        return attrs

    def create(self, validated_data: dict) -> Choice:
        return Choice.objects.create(**validated_data)

    def update(self, instance: Choice, validated_data: dict) -> Choice:
        instance.description = validated_data['description']
        instance.is_main_story = validated_data['is_main_story']
        instance.from_passage_id = validated_data['from_passage_id']
        instance.to_passage_id = validated_data['to_passage_id']
        instance.save()
        return instance

    @classmethod
    def for_instance(cls, instance_id: int, data: dict) -> 'ChoiceService':
        choice_instance = Choice.objects.get(pk=instance_id)
        return cls(choice_instance, data=data)
