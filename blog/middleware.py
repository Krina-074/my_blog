import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class BlogRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = now()
        logger.info(f"Request: {request.method} {request.path}")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        duration = (now() - start_time).total_seconds()
        logger.info(f"Response: {response.status_code} for {request.path} in {duration:.2f}s")

        return response