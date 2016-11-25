from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from main.models import Author, Book


class BookView(View):
    http_method_names = ['get', 'post', 'put', 'patch']
    parameter_error_resp = {
        'status': 400,
        'result': 'Missing or wrong parameter!'
    }
    authors_error_resp = {
        'status': 400,
        'result': 'Some author(s) cannot be found!'
    }
    book_error_resp = {
        'status': 404,
        'result': 'Book not found!'
    }

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(BookView, self).dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({
            'status': 405,
            'result': 'Invalid method!'
        }, status=405)

    def _validate(self, post_keys):
        required_keys = set(['title', 'lc_classification', 'authors'])
        return required_keys.issubset(set(post_keys))

    def _get_authors_or_fail(self, author_ids_str):
        ids = author_ids_str.split(',')
        authors = Author.objects.filter(pk__in=ids)
        if len(authors) != len(ids):
            return False
        return authors

    def get(self, request, id=None):
        resp = {'status': 404, 'result': None}
        if id:
            if Book.objects.filter(pk=id).exists():
                resp['result'] = Book.objects.get_from_id_with_authors(id)
                resp['status'] = 200

            return JsonResponse(resp, status=resp['status'])

        query_params = None
        if request.GET:
            query_params = {}
            for key, value in request.GET.items():
                if key == 'authors':
                    key += '__name'
                query_params['{0}__{1}'.format(key, 'icontains')] = value

        result = Book.objects.get_with_authors(query_params)
        if result:
            resp['status'] = 200
            resp['result'] = result

        return JsonResponse(resp, status=resp['status'])

    def post(self, request):
        post = request.POST
        if not self._validate(post.keys()):
            return JsonResponse(self.parameter_error_resp)

        authors = self._get_authors_or_fail(post['authors'])
        if not authors:
            return JsonResponse(self.authors_error_resp)

        new_book = Book.objects.create(
            title=post['title'],
            lc_classification=post['lc_classification']
        )
        new_book.authors.add(*authors)
        resp = {
            'status': 201,
            'result': Book.objects.get_from_id_with_authors(new_book.id)
        }
        return JsonResponse(resp, status=resp['status'])

    def put(self, request, id=None):
        post = request.POST
        if not self._validate(post.keys()):
            return JsonResponse(self.parameter_error_resp)

        authors = self._get_authors_or_fail(post['authors'])
        if not authors:
            return JsonResponse(self.authors_error_resp)

        del post['authors']
        book = Book(id=id)
        for key, value in post.items():
            setattr(book, key, value)
        book.save()
        book.authors.clear()
        book.authors.add(*authors)

        resp = {
            'status': 200,
            'result': Book.objects.get_from_id_with_authors(id)
        }
        return JsonResponse(resp)

    def patch(self, request, id=None):
        post = request.POST
        resp = {}
        try:
            book = Book.objects.get(pk=id)
        except ObjectDoesNotExist:
            return JsonResponse(self.book_error_resp)

        if post.get('authors'):
            authors = self._get_authors_or_fail(post['authors'])
            if not authors:
                return JsonResponse(self.authors_error_resp)
            book.authors.clear()
            del post['authors']

        for key, value in post.items():
            setattr(book, key, value)
        book.save()
        book.authors.add(*authors)

        resp = {
            'status': 200,
            'result': Book.objects.get_from_id_with_authors(id)
        }
        return JsonResponse(resp, status=resp['status'])
