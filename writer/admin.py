from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ['type', 'date', 'body', 'title']

admin.site.register(Post, PostAdmin)
