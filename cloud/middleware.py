import time

from cloud.services import build_request_stats_service


class RequestStatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_stats = build_request_stats_service()

        began_at = time.time()
        response = self.get_response(request)
        took_seconds = time.time() - began_at

        request_stats.incr_request_count()
        request_stats.incr_request_time(took_seconds)

        return response
