import os
import shutil

from datetime import date, timedelta
from pathlib import Path
from zipfile import ZipFile

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author, Chapter, PairingType, Story


class EpubExportsContentTestCase(TestCase):
    def setUp(self):
        PairingType.objects.create(pairing_type="oth", label="Autre")
        PairingType.objects.create(pairing_type="het", label="Hétéro")
        PairingType.objects.create(pairing_type="mm", label="M/M")
        PairingType.objects.create(pairing_type="ff", label="F/F")
        PairingType.objects.create(pairing_type="gen", label="Aucun")

        Member.objects.create_user(
            'Author1', email='author1@mail.fr', password='pass'
        )
        Member.objects.create_user(
            'Author2', email='author2@mail.fr', password='pass'
        )
        Author.objects.create(
            member=Member.objects.get(username="Author1"),
            nickname="Author1"
        )
        Author.objects.create(
            member=Member.objects.get(username="Author2"),
            nickname="Author2"
        )

        tomorrow = date.today() + timedelta(days=1)

        story1 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Visible By All Title", summary="Visible by all summary",
            rating="g", visibility="Everyone", story_author_note="<p>An author note</p>"
        )
        story1.pairing_type.set(PairingType.objects.filter(label="M/M"))
        Chapter.objects.create(story=story1, content="Test Content Story 1", number=1)
        Chapter.objects.create(
            story=story1,
            content="Test Content Chapter 2",
            number=2,
            chapter_title="My Beautiful Chapter 2 Title"
        )
        Chapter.objects.create(
            story=story1,
            content="Test Content Chapter 3",
            number=3,
            publishing_date=tomorrow
        )

        self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':1})
        )

        epub_dir_path = Path(settings.GENERATED_FILES_DIR)
        epub_path = epub_dir_path / f"{story1.author}_{story1.story_title}.epub"
        extract_dir_path = Path(settings.GENERATED_FILES_DIR) / "test_epub"
        extract_dir_path.mkdir(parents=True, exist_ok=True)
        
        with ZipFile(epub_path, 'r') as test_epub:
            test_epub.extractall(path=extract_dir_path)

    def tearDown(self):
        epub_dir_path = Path(settings.GENERATED_FILES_DIR) / "test_epub"
        with os.scandir(epub_dir_path) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                else:
                    os.remove(entry.path)

    """
        TEST CONTENT
        Testing that we get:
        - Visible chapters only
        - Story Author note
        - Chapter titles or not
        NOTE : because of the way epub works (not prologue, only chapter 1),
        chapter-2.xhtml refers to the "real" chapter 1. 
    """
    def test_export_content_only_visible_chapters_not_author(self):
        epub_content_path = Path(settings.GENERATED_FILES_DIR) / "test_epub/OEBPS"
        dir_list = os.listdir(epub_content_path)

        self.assertIn(
            "chapter-3.xhtml", dir_list
        )
        self.assertNotIn(
            "chapter-4.xhtml", dir_list
        )


    def test_export_content_only_visible_chapters_is_author(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':1})
        )

        story = Story.objects.get(pk=1)

        epub_dir_path = Path(settings.GENERATED_FILES_DIR) / "test_epub"
        epub_path = Path(settings.GENERATED_FILES_DIR) / f"{story.author}_{story.story_title}.epub"
        
        with ZipFile(epub_path, 'r') as test_epub:
            test_epub.extractall(path=epub_dir_path)

        epub_content_path = epub_dir_path / "OEBPS"
        dir_list = os.listdir(epub_content_path)

        self.assertIn(
            "chapter-4.xhtml", dir_list
        )

    def test_export_content_display_chapter_titles(self):
        """
            Checking chapters' title display correctly when
            there is one.
        """
        self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':1})
        )

        epub_dir_path = Path(settings.GENERATED_FILES_DIR) / "test_epub/OEBPS"
        chapter_file_path = epub_dir_path / "chapter-3.xhtml"

        with open(chapter_file_path) as f:
            chapter = f.read()
            self.assertIn(
                "Chapitre 2 : My Beautiful Chapter 2 Title", chapter
            )

    def test_export_content_foreword(self):
        """
            Foreword must contain:
            - the author's note
            - a link toward the original story
        """
        self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':1})
        )

        epub_dir_path = Path(settings.GENERATED_FILES_DIR)
        foreword_file_path = epub_dir_path / "test_epub/OEBPS/chapter-1.xhtml"

        with open(foreword_file_path) as f:
            foreword = f.read()
            self.assertIn('/1/1">son site d\'origine</a>', foreword)
            self.assertIn("An author note", foreword)