from analytics.models import APIRequestLog

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.path.startswith('/api/'):
            APIRequestLog.objects.create(
                user=request.user,
                endpoint=request.path,
                method=request.method,
            )
        return response
