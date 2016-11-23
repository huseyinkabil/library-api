from django.http.multipartparser import MultiPartParser


class HttpPatchAndPutMiddleware(object):
    METHODS = ('PATCH', 'PUT')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in self.METHODS:
            parser = MultiPartParser(
                request.META,
                request._stream,
                request.upload_handlers,
                request.encoding
            )
            request._post, request._files = parser.parse()

        response = self.get_response(request)

        return response
