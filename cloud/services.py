import os

from django_redis import get_redis_connection

DEFAULT_EXPIRE_TIME = 60 * 60  # 1 hour


class RequestStatsService:
    def __init__(self, redis, pid, expire_time):
        self.redis = redis
        self.pid = pid
        self.expire_time = expire_time

    def _get_request_count_key(self):
        return f"{self.pid}-request-count"

    def _get_request_time_key(self):
        return f"{self.pid}-request-time"

    def get_request_count(self):
        return int(self.redis.get(self._get_request_count_key()))

    def get_request_time(self):
        return float(self.redis.get(self._get_request_time_key()))

    def get_average_request_time(self):
        return self.get_request_time() / self.get_request_count()

    def incr_request_count(self):
        self.redis.incr(self._get_request_count_key())

    def incr_request_time(self, amount):
        self.redis.incrbyfloat(self._get_request_time_key(), amount)


def build_request_stats_service(expire_time=DEFAULT_EXPIRE_TIME):
    return RequestStatsService(
        redis=get_redis_connection("default"), pid=os.getcwd(), expire_time=expire_time,
    )
