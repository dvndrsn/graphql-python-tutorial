from django.contrib import admin

from .models import Story, Passage, Choice, Character, Author

# Register your models here.
admin.site.register(Story)
admin.site.register(Passage)
admin.site.register(Choice)
admin.site.register(Character)
admin.site.register(Author)
