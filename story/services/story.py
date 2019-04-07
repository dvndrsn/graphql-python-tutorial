from rest_framework import serializers

from story.models import Author, Story


class StoryService(serializers.Serializer):
    title = serializers.CharField()
    subtitle = serializers.CharField()
    description = serializers.CharField()
    published_date = serializers.DateField()
    author_id = serializers.IntegerField()

    def validate_author_id(self, author_id: int) -> int:
        try:
            Author.objects.get(pk=author_id)
            return author_id
        except Author.DoesNotExist:
            raise serializers.ValidationError('Author does not exist')

    def create(self, validated_data: dict) -> Story:
        return Story.objects.create(**validated_data)

    def update(self, instance: Story, validated_data: dict) -> Story:
        instance.title = validated_data['title']
        instance.subtitle = validated_data['subtitle']
        instance.description = validated_data['description']
        instance.published_date = validated_data['published_date']
        instance.author_id = validated_data['author_id']
        instance.save()
        return instance

    @classmethod
    def for_instance(cls, instance_id: int, data: dict) -> 'StoryService':
        story_instance = Story.objects.get(pk=instance_id)
        return cls(story_instance, data=data)
