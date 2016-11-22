from django.http.multipartparser import MultiPartParser


class HttpPatchMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PATCH':
            parser = MultiPartParser(
                request.META,
                request._stream,
                request.upload_handlers,
                request.encoding
            )
            request._post, request._files = parser.parse()

        response = self.get_response(request)

        return response
