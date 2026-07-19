from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from archives.models import Story


def story_for_html_export(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    story_url = reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1})
    full_story_url = request.build_absolute_uri(story_url)

    return render(
            request,
            'archives/story_html_export.html',
            {"story": story, "url": full_story_url}
    )

def export_html(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    file_title = f"{story.author}_{story.story_title}"
    story_html = story_for_html_export(request, story_id)

    return HttpResponse(
        story_html,
        content_type='text/html',
        headers={
            'Content-Disposition': f'attachment; filename="{file_title}.html"'
        },
    )