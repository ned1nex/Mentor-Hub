import logging
import sys
from redis import Redis
from .config import config

# Настройка логгера для вывода логов в консоль
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

db = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT
)

def get_cache():
    try:
        yield db
    except Exception as e:
        logger.exception("Ошибка в зависимости get_cache: %s", e)
        raise e
    finally:
        db.close()
