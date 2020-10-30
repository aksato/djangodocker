from django.shortcuts import render
from django.conf import settings
import time
import redis

# connect to our Redis instance
cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def homePageView(request):
    count = get_hit_count()
    return render(request, "index.html", context={})