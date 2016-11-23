from django.http import HttpResponse, JsonResponse
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
