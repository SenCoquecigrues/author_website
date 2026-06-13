from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'archives'

urlpatterns = [
    path('', login_required(views.Index.as_view()), name='index'),
    # path('<int:author_id>', login_required(views.Index.as_view()), name="author_bibliography"),
    # Story
    # path('library/publish', login_required(views.StoryPublishView.as_view()), name="publish_story"),
    # path('library/<int:story_id>/<int:chapter_number>', views.StoryReadView.as_view(), name="read_story"),
    # path('library/<int:story_id>/edit', login_required(views.StoryEditView.as_view()), name="edit_story"),
    # path('library/<int:story_id>/delete', login_required(views.story_delete), name="story_delete"),
    # # Chapter
    # path('library/<int:story_id>/publish', login_required(views.ChapterPostView.as_view()), name="publish_chapter"),
    # path('library/<int:story_id>/chapter/<int:chapter_number>/edit', login_required(views.ChapterEditView.as_view()), name="edit_chapter"),
    # path('library/<int:chapter_id>/delete', login_required(views.chapter_delete), name="chapter_delete"),
]