from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row
from .config import get_settings


def connect():
    settings = get_settings()
    try:
        password = settings.db_password_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError("Database secret is unavailable") from exc
    if not password:
        raise RuntimeError("Database secret is empty")
    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=password,
        row_factory=dict_row,
        connect_timeout=5,
    )


@contextmanager
def transaction():
    with connect() as connection:
        with connection.transaction():
            yield connection
