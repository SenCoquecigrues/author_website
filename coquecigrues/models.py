from django.db import models

from accounts.models import Member


class Roleplayer(models.Model):
    """
        This class is to use for plugging the app into
        any Django project. Link member to your user model.
    """
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="roleplayer_profile"
    )
    is_adult = models.BooleanField(
        default=False
    )

class World(models.Model):
    VISIBILITY_CHOICES = [
        ('p', 'private'),
        ('a', 'admin team'),
        ('e', 'everyone')
    ]
    RATING_CHOICES = [
        ('e', 'explicit'),
        ('a', 'adult'),
        ('t', 'teens'),
        ('e', 'everyone')
    ]
    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default='p'
    )
    open_for_play = models.BooleanField(default=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    rating = models.CharField(
        max_length=2,
        choices=RATING_CHOICES,
        default='t'
    )
    participants = models.ManyToManyField(
        Roleplayer,
        blank=True,
        related_name="world_where_playing")
    creator = models.ForeignKey(
        Roleplayer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_world"
    )

    def __str__(self):
        return self.name