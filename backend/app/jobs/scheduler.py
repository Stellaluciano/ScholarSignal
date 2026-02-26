import time

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

from app.config import settings

if __name__ == "__main__":
    redis = Redis.from_url(settings.redis_url)
    q = Queue("default", connection=redis)
    s = Scheduler(queue=q, connection=redis)
    # placeholder recurring jobs could be set here.
    while True:
        time.sleep(60)
