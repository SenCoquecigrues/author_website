from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ['post_type', 'date', 'body', 'title']

admin.site.register(Post, PostAdmin)
