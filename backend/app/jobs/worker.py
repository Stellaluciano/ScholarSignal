from redis import Redis
from rq import Worker

from app.config import settings


if __name__ == "__main__":
    Worker(["default"], connection=Redis.from_url(settings.redis_url)).work()
