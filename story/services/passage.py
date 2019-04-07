from rest_framework import serializers

from story.models import Passage, Story, Character


class PassageService(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    is_ending = serializers.BooleanField()
    story_id = serializers.IntegerField()
    character_id = serializers.IntegerField()

    def validate_story_id(self, story_id: int) -> int:
        try:
            Story.objects.get(pk=story_id)
            return story_id
        except Story.DoesNotExist:
            raise serializers.ValidationError('Story does not exist')

    def validate_character_id(self, character_id: int) -> int:
        try:
            Character.objects.get(pk=character_id)
            return character_id
        except Character.DoesNotExist:
            raise serializers.ValidationError('Character does not exist')

    def create(self, validated_data: dict) -> Passage:
        return Passage.objects.create(**validated_data)

    def update(self, instance: Passage, validated_data: dict) -> Passage:
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.is_ending = validated_data['is_ending']
        instance.story_id = validated_data['story_id']
        instance.pov_character_id = validated_data['character_id']
        instance.save()
        return instance

    @classmethod
    def for_instance(cls, instance_id: int, data: dict) -> 'PassageService':
        passage_instance = Passage.objects.get(pk=instance_id)
        return cls(passage_instance, data=data)
