from django.db import models

class Post(models.Model):
    POST_TYPES = {
        "NE": "News",
        "WR": "Writing",
        "AU": "Authorship"
    }

    post_type = models.CharField(
        max_length=2,
        choices=POST_TYPES,
        default="NE"
    )
    date = models.DateField()
    title = models.CharField(default="", blank=True, max_length=200)
    body = models.TextField(max_length=6000)
    
    def __str__(self): # pragma: no cover
        return f"{self.date} : {self.body[:100]}..."
