from __future__ import unicode_literals

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_date = models.DateField()


class Book(models.Model):
    title = models.CharField(max_length=255)
    lc_classification = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
