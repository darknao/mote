import logging
import os

import rq
from fedora_messaging.api import consume
from fedora_messaging.config import conf
from redis import Redis

conf.setup_logging()
REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
redis = Redis.from_url(REDIS_URL)
task_queue = rq.Queue("tasks", connection=redis, default_timeout=60 * 10)


def consume_fedora_messaging_msg(message):
    logging.info(message)
    task_queue.enqueue("mote.tasks.process_new_meet", args=(message.body,))


if __name__ == "__main__":
    conf.setup_logging()
    consume(consume_fedora_messaging_msg)