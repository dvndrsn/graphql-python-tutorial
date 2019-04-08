from datetime import date
from typing import Any

import graphene

from story.models import Author
from story.services import StoryService


class CreateStory(graphene.Mutation):

    class Arguments:
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'CreateStory':
        published_year = int(input_data['published_year']) # type: ignore
        author = Author.objects.get(pk=4)
        serializer = StoryService(data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_date': date(year=published_year, month=1, day=1),
            'author_id': author.pk
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story)


class UpdateStory(graphene.Mutation):

    class Arguments:
        story_id = graphene.ID()
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()
        author_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'UpdateStory':
        story = int(input_data['story_id']) # type: ignore
        published_year = int(input_data['published_year']) # type: ignore
        author = Author.objects.get(pk=4)
        serializer = StoryService.for_instance(story, data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_date': date(year=published_year, month=1, day=1),
            'author_id': author.pk
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story)


class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
