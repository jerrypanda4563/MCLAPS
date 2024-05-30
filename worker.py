from app.redis_config import cache
from rq import Worker, Queue, Connection
import logging

listen = ['default']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_conn = cache

if __name__ == '__main__':
    logger.info('Worker starting...')
    try:
        with Connection(redis_conn):
            worker = Worker(map(Queue, listen))
            worker.work()
    except Exception as e:
        logger.error(f'Worker failed: {e}')
        raise e