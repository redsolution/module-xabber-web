from django.db import models


class XabberWebSettings(models.Model):
    key = models.TextField(unique=True)
    value = models.TextField()
