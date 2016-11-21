import csv
import itertools
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from main.models import Book, Author


class LibraryView(View):
    http_method_names = ['post', 'patch']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LibraryView, self).dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request):
        return JsonResponse({
            'error_message': 'Method not allowed!',
            'allowed_methods': self._allowed_methods(),
        }, status=405)

    def _clear_database(self):
        Book.objects.raw('TRUNCATE TABLE ')
        Author.objects.all().delete()

    def _grouper(self, iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return itertools.izip_longest(fillvalue=fillvalue, *args)

    def _insert_author_from_tuple(self, author):
        return Author.objects.create(
            name=author[0],
            surname=author[1],
            birth_date=author[2]
        )

    def post(self, request, *args, **kwargs):
        self._clear_database()
        rows = csv.reader(request.FILES.get('library'))
        book_count, author_count = (0, 0)
        for row in rows:
            book = row[:2]
            book_obj = Book.objects.create(
                title=book[0],
                lc_classification=book[1]
            )
            if book_obj is not None:
                book_count += 1
                authors = list(self._grouper(row[2:], 3))
                author_count = 0
                for author in authors:
                    if book_obj.authors.add(
                            self._insert_author_from_tuple(author)):
                        author_count += 1

        msg = '{} books and {} authors are inserted!'.format(
            book_count,
            author_count
        )
        return JsonResponse({'status': 'succeeded', 'message': msg})

    def patch(self, request):
        return JsonResponse({'status': 'succeeded, patch'})
