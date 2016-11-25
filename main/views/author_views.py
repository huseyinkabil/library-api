from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import Error
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.models import Author


class AuthorView(View):
    http_method_names = ['get', 'post', 'put', 'patch']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AuthorView, self).dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({
            'status': 405,
            'result': 'Invalid method!',
            'allowed_methods': ','.join(self.http_method_names)
        }, status=405)

    def _validate(self, post_keys):
        required_keys = {'name', 'surname', 'birth_date'}
        return required_keys.issubset(set(post_keys))

    def get(self, request, id=None):
        if id:
            try:
                author = Author.objects.get(pk=id)
            except ObjectDoesNotExist as e:
                resp = {'status': 404, 'result': e.message}
            else:
                resp = {'status': 200, 'result': author.to_dict()}
            return JsonResponse(resp, status=resp['status'])

        query_params = None
        if request.GET:
            query_params = {}
            for key, value in request.GET.items():
                query_params['{0}__{1}'.format(key, 'icontains')] = value

        authors = Author.objects.filter(**query_params)

        resp = {
            'status': 200,
            'result': [a.to_dict() for a in authors]
        }
        return JsonResponse(resp, status=resp['status'])

    def post(self, request):
        post = request.POST
        if not self._validate(post.keys()):
            return JsonResponse({
                'status': 400,
                'result': 'Missing or wrong parameter!'
            })
        resp = {
            'status': 201
        }
        try:
            author = Author.objects.create(
                name=post['name'],
                surname=post['surname'],
                birth_date=post['birth_date']
            )
            resp['result'] = author.to_dict()
        except (Error, ValidationError) as e:
            resp['status'] = 404
            resp['result'] = e.message

        return JsonResponse(resp, status=resp['status'])

    def put(self, request, id=None):
        resp = {'status': 200}
        try:
            author = Author.objects.get(pk=id)
        except ObjectDoesNotExist as e:
            resp['status'] = 404
            resp['result'] = e.message
            return JsonResponse(resp, status=resp['status'])

        author = Author(id=id)
        for key, value in request.POST.items():
            setattr(author, key, value)

        try:
            author.save()
        except (Error, ValidationError) as e:
            resp['result'] = e.message
            return JsonResponse(resp, status=resp['status'])

        resp['result'] = author.to_dict()
        return JsonResponse(resp, status=resp['status'])

    def patch(self, request, id=None):
        resp = {'status': 200}
        try:
            author = Author.objects.get(pk=id)
        except ObjectDoesNotExist as e:
            resp['status'] = 404
            resp['result'] = e.message
            return JsonResponse(resp, status=resp['status'])

        for key, value in request.POST.items():
            setattr(author, key, value)

        try:
            author.save()
        except (Error, ValidationError) as e:
            resp['result'] = e.message
            return JsonResponse(resp, status=resp['status'])

        resp['result'] = author.to_dict()
        return JsonResponse(resp, status=resp['status'])
