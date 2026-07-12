import datetime

from django.db import models

from accounts.models import Member


class PairingType(models.Model):
    pairing_type = models.CharField(max_length=5, unique=True)
    label = models.CharField(max_length=10)

    def __str__(self):
        return self.label


class Author(models.Model):
    member = models.ForeignKey(Member,
        on_delete=models.CASCADE,
        null=True)
    nickname = models.CharField(
        max_length=100, unique=True
    )
    criminal = models.BooleanField(default=False)
    trackbear_profile = models.CharField(
        max_length=100, default='', blank=True
    )
    trackbear_api_key = models.CharField(
        max_length=100, default='', blank=True
    )

    other_profile_url = models.CharField(
        max_length=100, default='', blank=True
    )

    def __str__(self):
        return self.nickname


class Reader(models.Model):
    serif = models.BooleanField(default=True)
    font_size = models.FloatField(default=1.0)
    member = models.OneToOneField(
        Member, 
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="reader_profile"
    )


class Story(models.Model):
    RATING_CHOICES = [
        ('g', 'Tout public'),
        ('t', 'Public averti'),
        ('e', 'Explicite')
    ]

    VISIBILITY_CHOICES = [
        ("Private", "Privée"),
        ("Members only", "Membres seules"),
        ("Everyone", "Visibles par tous")
    ]
    
    LENGTH_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('novella', 'Novella'),
        ('roman', 'Roman'),
        ('series', 'Série')
    ]

    author = models.ForeignKey(Author,
        on_delete=models.CASCADE,
        null=True, blank=True)
    clap = models.IntegerField(default=0, blank=True)
    story_date = models.DateField(null=True, default=datetime.date.today)
    story_title = models.CharField(max_length=150)
    summary = models.TextField(max_length=600)
    story_author_note = models.TextField(max_length=2000, blank=True)
    pairing_archetype = models.CharField(max_length=200, blank=True)
    one_sentence_summary = models.CharField(max_length=200, blank=True)
    pairing_type = models.ManyToManyField(
        PairingType, 
        blank=True,
    )
    rating = models.CharField(
        max_length=6,
        choices=RATING_CHOICES,
        default='g'
    )
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="Members only"
    )
    text_length = models.CharField(
        max_length=20,
        choices=LENGTH_CHOICES,
        default='nouvelle'
    )
    complete = models.BooleanField(default=True)

    @property
    def has_multiple_chapters(self):
        if Chapter.objects.filter(story=self).count() > 1:
            return True
        return False
    
    @property
    def first_chapter(self):
        return Chapter.objects.filter(story=self, number=1)[0]

    @property
    def number_of_chapter(self):
        return Chapter.objects.filter(story=self).count()

    def __str__(self):
        return f"{self.author} : {self.story_title}"

    class Meta:
        verbose_name_plural = 'stories'


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, related_name="chapters")
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    chapter_title = models.CharField(max_length=150, null=True, blank=True)
    chapter_author_note = models.TextField(max_length=1500, null=True, blank=True)
    content = models.TextField(max_length=1000000)
    publishing_date = models.DateField(null=True, default=datetime.date.today)

    def __str__(self):
        return f"{self.story}, chapter {self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'number'], name="unique_chapter_number_for_story")
        ]


class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=True, related_name="comments")
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="comments")
    content = models.TextField(max_length=3000)


class Reaction(models.Model):
    text_emoji = models.CharField(max_length=20)

    def __str__(self):
        return self.text_emoji


class ReactionsRelationships(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="member_reacted_as"
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="story_reacted_as"
    )
    reaction = models.ForeignKey(
        Reaction,
        on_delete=models.CASCADE,
        related_name="reacted_as"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'member'], name="members_can_only_react_one_way")
        ]
