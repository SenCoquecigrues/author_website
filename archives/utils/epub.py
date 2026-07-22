from pathlib import Path

import pypub
from django.conf import settings
from pypub.factory import SUPPORTED_TAGS


class EpubFormatter():
    def create_epub(story, file_title: str, foreword: bytes, chapters: list[tuple]):
        epub = pypub.Epub(
            language = "fr",
            rights="CC BY-NC-ND",
            publisher= "Une Petite Voiture Noire",
            title = story.story_title,
            creator = story.author.nickname,
            date=story.story_date
        )

        SUPPORTED_TAGS['p'] = ('style', 'a')

        foreword = pypub.create_chapter_from_html(foreword, title="Avant-propos")
        epub.add_chapter(foreword)

        for chapter_title, chapter_content in chapters:
            chapter = pypub.create_chapter_from_html(chapter_content, title=chapter_title)
            epub.add_chapter(chapter)

        epub_path = Path(settings.GENERATED_FILES_DIR) / f"{file_title}.epub"

        epub.create(epub_path)

    def formatted_chapter_title(chapter, is_oneshot: bool):
        if is_oneshot:
            return chapter.story.title

        title = f"Chapitre {chapter.number}"
        if chapter.chapter_title:
            title += f" : {chapter.chapter_title}"
        return title

    def format_content(content: str) -> str:
        content = content.replace('class="ql-align-right"', 'style="text-align: right"')
        content = content.replace('class="ql-align-left"', 'style="text-align: left}"')
        content = content.replace('class="ql-align-justify"', 'style="text-align: justify"')
        content = content.replace('class="ql-align-center"', 'style="text-align: center"')

        return content

    # def get_epub_path():
    #     current_path = Path.cwd()
    #     depth = 1
    #     root_folder = cwd.parents[n - depth]