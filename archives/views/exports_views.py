import logging

from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from archives.models import Story
from archives.utils.epub import EpubFormatter

def story_for_html_export(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    story_url = reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1})
    full_story_url = request.build_absolute_uri(story_url)

    return render(
            request,
            'archives/exports/html_story.html',
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

def foreword_epub_export(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    story_url = reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1})
    full_story_url = request.build_absolute_uri(story_url)
    formatted_author_note = EpubFormatter.format_content(story.story_author_note)
    return render(
            request,
            'archives/exports/epub_author_note.html',
            {"story": story, "full_story_url": full_story_url, "author_note":formatted_author_note}
    )

def export_epub_chapter(request, chapter):
    formatted_chapter = EpubFormatter.format_content(chapter.content)

    return render(
            request,
            'archives/exports/epub_chapter.html',
            {"chapter_content": formatted_chapter}
    )

def export_epub(request, story_id):
    try:
        story = get_object_or_404(Story, id=story_id)
        file_title = f"{story.author}_{story.story_title}"
        number_of_chapters = story.chapters.count()

        if not number_of_chapters:
            logging.error(
                f"Error while attempting epub export for story {story}: no chapters found."
            )
            raise ValueError("Aucun chapitre trouvé !") 

        epub_path = Path(settings.GENERATED_FILES_DIR) / f"{file_title}.epub"

        foreword = foreword_epub_export(request, story_id).content
        list_of_html_chapters = [
            (
                EpubFormatter.formatted_chapter_title(chapter, number_of_chapters ==1),
                export_epub_chapter(request, chapter).content
            ) for chapter in story.chapters.all()
        ]

        EpubFormatter.create_epub(story, file_title, foreword, list_of_html_chapters)

        return FileResponse(
            open(epub_path, "rb"),
            as_attachment=True,
            filename=f"{file_title}.epub",
        )

    except Exception as e:
        logging.error(f"Error while attempting to export {file_title} : {e}")
        return HttpResponse(
            f"L'export a échoué car Sen est une misérable. Contactez-la. Regardez-la droit dans les yeux. (erreur : {e})",
            content_type='text/plain',
            headers={
                'Content-Disposition': 'attachment; filename="export_failed.txt"'
            },
        )