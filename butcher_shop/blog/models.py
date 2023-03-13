from django.db import models

from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=250)
    preview = RichTextField(max_length=500, default="")
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_receipt = models.BooleanField(default=False)

