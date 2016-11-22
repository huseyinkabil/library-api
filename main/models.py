from __future__ import unicode_literals

from django.db import models


class AuthorManager(models.Manager):
    def create_author(self, author_tuple):
        author, created = Author.objects.get_or_create(
            name=author_tuple[0],
            surname=author_tuple[1],
            birth_date=author_tuple[2]
        )
        return author

    def create_authors(self, authors):
        return [self.create_author(a) for a in authors]


class Author(models.Model):
    objects = AuthorManager()
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_date = models.DateField()

    def __unicode__(self):
        return '{} {}, {}'.format(self.name, self.surname, self.birth_date)


class Book(models.Model):
    title = models.CharField(max_length=255)
    lc_classification = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Author)

    def __unicode__(self):
        return self.name
