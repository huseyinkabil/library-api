import csv
import itertools
from django.db import transaction
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
        with transaction.atomic():
            Book.objects.all().delete()
            Author.objects.all().delete()

    def _grouper(self, iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return itertools.izip_longest(fillvalue=fillvalue, *args)

    def _import_csv_to_db(self, csv_file):
        with csv_file:
            rows = csv.reader(csv_file)
            book_count = 0
            for row in rows:
                book = row[:2]
                new_book, created = Book.objects.get_or_create(
                    title=book[0],
                    lc_classification=book[1],
                )
                if created:  # If created is true, book is created now.
                    book_count += 1
                    authors = list(self._grouper(row[2:], 3))
                    authors = Author.objects.create_authors(authors)
                    new_book.authors.add(*authors)

        return '{} books are inserted!'.format(book_count)

    def post(self, request, *args, **kwargs):
        self._clear_database()
        f = request.FILES.get('library')
        msg = self._import_csv_to_db(f)
        return JsonResponse({'status': 'succeeded', 'message': msg})

    def patch(self, request, *args, **kwargs):
        f = request.FILES.get('library')
        msg = self._import_csv_to_db(f)
        return JsonResponse({'status': 'succeeded', 'message': msg})
