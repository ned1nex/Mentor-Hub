import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import config

# Настраиваем логгер для вывода логов в консоль
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаём обработчик, который выводит логи в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Формирование строки подключения к БД
DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"
engine = create_engine(
    DATABASE_URI.format(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        db=config.POSTGRES_DB,
    )
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.exception(f"Ошибка в зависимости get_db: {e}")
        raise e
    finally:
        db.close()
