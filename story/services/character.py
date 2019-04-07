from rest_framework import serializers

from story.models import Character


class CharacterService(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data: dict) -> Character:
        return Character.objects.create(**validated_data)

    def update(self, instance: Character, validated_data: dict) -> Character:
        instance.name = validated_data['name']
        instance.save()
        return instance

    @classmethod
    def for_instance(cls, instance_id: int, data: dict) -> 'CharacterService':
        character_instance = Character.objects.get(pk=instance_id)
        return cls(character_instance, data=data)
