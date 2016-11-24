from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from main.models import Author, Book


class BookView(View):
    http_method_names = ['get', 'post', 'put', 'patch']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(BookView, self).dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({
            'status': 405,
            'result': 'Invalid method!'
        }, status=405)

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
        required_keys = set(['title', 'authors'])

        resp = {
            'status': 400,
            'result': 'Missing or wrong parameter!'
        }
        if not required_keys.issubset(set(post.keys())):
            return JsonResponse(resp, status=resp['status'])

        authors_ids = post.get('authors').split(',')
        authors = Author.objects.filter(pk__in=authors_ids)
        if len(authors) != len(authors_ids):
            resp['result'] = 'Some author(s) cannot be found!'
            return JsonResponse(resp, status=resp['status'])

        try:
            new_book = Book.objects.create(
                title=post['title'],
                lc_classification=get_random_string()
            )
        except IntegrityError:
            resp['result'] = 'An error occured, please try again!'
            return JsonResponse(resp, status=resp['status'])

        new_book.authors.add(*authors)
        resp['status'] = 201
        resp['result'] = Book.objects.get_from_id_with_authors(new_book.id)

        return JsonResponse(resp, status=resp['status'])
