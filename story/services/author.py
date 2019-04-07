from rest_framework import serializers

from story.models import Author


class AuthorService(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    twitter_account = serializers.CharField()

    def create(self, validated_data: dict) -> Author:
        return Author.objects.create(**validated_data)

    def update(self, instance: Author, validated_data: dict) -> Author:
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.twitter_account = validated_data['twitter_account']
        instance.save()
        return instance

    @classmethod
    def for_instance(cls, instance_id: int, data: dict) -> 'AuthorService':
        author_instance = Author.objects.get(pk=instance_id)
        return cls(author_instance, data=data)
