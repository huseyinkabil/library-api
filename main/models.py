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

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'birth_date': self.birth_date
        }


class BookManager(models.Manager):
    def get_from_id_with_authors(self, id=None):
        if not id:
            return None

        book = Book.objects.filter(pk=id).prefetch_related('authors')[0]
        book_dict = book.to_dict()
        for a in book.authors.all():
            book_dict['authors'].append(a.to_dict())
        return book_dict

    def get_with_authors(self, lookups=None):
        books = Book.objects.prefetch_related('authors')
        if lookups:
            books = books.filter(**lookups)

        result = []
        for b in books:
            b_dict = b.to_dict()
            for a in b.authors.all():
                b_dict['authors'].append(a.to_dict())
            result.append(b_dict)

        return result


class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=255)
    lc_classification = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Author)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'title': self.title,
            'lc_classification': self.lc_classification,
            'authors': []
        }
