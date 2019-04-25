from datetime import date
from typing import Any

import graphene

from story.services import StoryService
from story.models import Story

from api.utils import from_global_id


class CreateStory(graphene.ClientIDMutation):

    class Input:
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()
        author_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')
    author = graphene.Field('api.query.author.AuthorType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'CreateStory':
        published_year = int(input_data['published_year']) # type: ignore
        serializer = StoryService(data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_date': date(year=published_year, month=1, day=1),
            'author_id': from_global_id(input_data['author_id']).type_id
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story, author=story.author)


class UpdateStory(graphene.ClientIDMutation):

    class Input:
        story_id = graphene.ID()
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()
        author_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')
    author = graphene.Field('api.query.author.AuthorType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'UpdateStory':
        story = int(input_data['story_id']) # type: ignore
        published_year = int(input_data['published_year']) # type: ignore
        serializer = StoryService.for_instance(story, data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_date': date(year=published_year, month=1, day=1),
            'author_id': from_global_id(input_data['author_id']).type_id
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story, author=story.author)


class DeleteStory(graphene.ClientIDMutation):

    class Input:
        story_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')
    author = graphene.Field('api.query.author.AuthorType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'UpdateStory':
        story_id = from_global_id(input_data['story_id']).type_id
        story = Story.objects.get(pk=story_id)
        story.delete()
        return cls(story=story, author=story.author)



class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
    delete_story = DeleteStory.Field()
