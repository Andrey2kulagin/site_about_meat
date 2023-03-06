from django.db import models

from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=250)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
