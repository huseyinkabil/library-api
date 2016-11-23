from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from main.models import Book


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
                resp['result'] = Book.objects.filter(pk=id).values()[0]
                resp['status'] = 200

            return JsonResponse(resp, status=resp['status'])

        if request.GET:
            query_params = {}
            for key, value in request.GET.items():
                query_params['{0}__{1}'.format(key, 'contains')] = value
            books = Book.objects.filter(**query_params).values()
        else:
            books = Book.objects.all().values()

        if books:
            resp['status'] = 200
            resp['result'] = list(books)

        return JsonResponse(resp, status=resp['status'])
