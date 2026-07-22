from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'archives'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('author/<int:author_id>', login_required(views.Index.as_view()), name="author_bibliography"),
    # Story
    path('publish', login_required(views.StoryPublishView.as_view()), name="publish_story"),
    path('<int:story_id>/<int:chapter_number>', views.StoryReadView.as_view(), name="read_story"),
    path("<int:story_id>/clap", views.clap_story, name="clap"),
    path('<int:story_id>/edit', login_required(views.StoryEditView.as_view()), name="edit_story"),
    path('<int:story_id>/delete', login_required(views.story_delete), name="story_delete"),
    # Chapter
    path('<int:story_id>/publish', login_required(views.ChapterPostView.as_view()), name="publish_chapter"),
    path("<int:chapter_id>/react_to_chapter", login_required(views.react_to_chapter), name="react_to_chapter"),
    path('<int:story_id>/chapter/<int:chapter_number>/edit', login_required(views.ChapterEditView.as_view()), name="edit_chapter"),
    path('<int:chapter_id>/delete', login_required(views.chapter_delete), name="chapter_delete"),
    # Exports
    path("<int:story_id>/epub", views.export_epub, name="export_epub"),
    path("<int:story_id>/epub_foreword", views.foreword_epub_export, name="epub_foreword"),
    path("<int:story_id>/epub_chapter", views.export_epub_chapter, name="epub_chapter"),
    path("<int:story_id>/html", views.export_html, name="export_html"),
    path("<int:story_id>/html_for_export", views.story_for_html_export, name="story_for_html_export")
]