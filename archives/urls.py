from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'archives'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('author/<int:author_id>', login_required(views.Index.as_view()), name="author_bibliography"),
    # TODO : à ranger plus tard
    # path("<int:story_id>/html", views.download_html, name="download_html"),
    # path("<int:story_id>/clap", views.clap, name="clap"),
    # Story
    path('publish', login_required(views.StoryPublishView.as_view()), name="publish_story"),
    path('<int:story_id>/<int:chapter_number>', views.StoryReadView.as_view(), name="read_story"),
    path('<int:story_id>/edit', login_required(views.StoryEditView.as_view()), name="edit_story"),
    path('<int:story_id>/delete', login_required(views.story_delete), name="story_delete"),
    # Chapter
    path('<int:story_id>/publish', login_required(views.ChapterPostView.as_view()), name="publish_chapter"),
    path('<int:story_id>/chapter/<int:chapter_number>/edit', login_required(views.ChapterEditView.as_view()), name="edit_chapter"),
    path('<int:chapter_id>/delete', login_required(views.chapter_delete), name="chapter_delete"),
]