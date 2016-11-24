from django.http.multipartparser import MultiPartParser
from django.http.multipartparser import MultiPartParserError
from django.http import JsonResponse


class HttpPatchAndPutMiddleware(object):
    METHODS = ('PATCH', 'PUT')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in self.METHODS:
            try:
                parser = MultiPartParser(
                    request.META,
                    request._stream,
                    request.upload_handlers,
                    request.encoding
                )
                request._post, request._files = parser.parse()
            except MultiPartParserError as e:
                return JsonResponse({
                    'status': 400,
                    'result': str(e)
                }, status=400)

        response = self.get_response(request)

        return response
