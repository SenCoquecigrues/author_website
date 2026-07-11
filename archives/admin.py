from django.contrib import admin
from .models import Author, Chapter, Reaction, ReactionsRelationships, Reader, Story, PairingType


class ChapterAdmin(admin.ModelAdmin):
    fields = [
        'story', 'chapter_title', 'number', 'content', 'chapter_author_note'
    ]


class StoryAdmin(admin.ModelAdmin):
    fields = ['author', 'story_title', 'story_date', 'summary',
        'story_author_note', 'pairing_type', 'rating',
        'visibility', 'text_length', 
        'complete', 'clap',
        'pairing_archetype', 'one_sentence_summary']
    list_display = ('story_title', 'author', 'story_date', 'complete', 'clap')
    list_filter = ('story_title', 'author', 'complete', 'visibility')


class PairingTypeAdmin(admin.ModelAdmin):
    fields = ['pairing_type', 'label']


admin.site.register(Author)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Reader)
admin.site.register(Reaction)
admin.site.register(ReactionsRelationships)
admin.site.register(Story, StoryAdmin)
admin.site.register(PairingType, PairingTypeAdmin)
