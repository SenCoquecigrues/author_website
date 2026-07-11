# from ebooklib import epub

from .models import Story, Chapter
from .utils_constants import html_fic_base, numbered_chapter_title, pdf_fic_base, pdf_page_title_style, pdf_normal_page_style


class StoryDigester:
    def __init__(self, story_id):
        self.fic = Story.objects.get(id=story_id)

    def return_title(self):
        return f"{self.fic.story_title}_par_{self.fic.author}"

    def html_fic(self):
        fic = self.fic
        results = html_fic_base.format(
            title=fic.story_title,
            author=fic.author,
            summary=fic.summary,
            chapters=self.html_chapter()
        )

        return results
    
    def html_chapter(self):
        chapters = Chapter.objects.filter(
            fic=self.fic.id).order_by('id')
        formatted_chapters = []
        i = 1

        if len(chapters) == 1:
            return chapters[0].content
        else:
            for chapter in chapters:
                formatted_chapters.append(
                    numbered_chapter_title.format(number=i) + chapter.content
                    )
                i += 1

            return "".join(formatted_chapters)

    def pdf_chapter(self):
        chapters = Chapter.objects.filter(
            fic=self.fic.id).order_by('id')
        formatted_chapters = []
        i = 1

        if len(chapters) == 1:
            return chapters[0].content
        else:
            for chapter in chapters:
                formatted_chapters.append(
                    numbered_chapter_title.format(number=i) + chapter.content
                    )
                i += 1

            return "".join(formatted_chapters)

    def pdf_fic(self):
        fic = self.fic
        results = pdf_fic_base.format(
            pdf_page_title_style=pdf_page_title_style,
            pdf_normal_page_style=pdf_normal_page_style,
            title=fic.story_title,
            author=fic.author,
            summary=fic.summary,
            chapters=self.pdf_chapter()
            )

        return results
