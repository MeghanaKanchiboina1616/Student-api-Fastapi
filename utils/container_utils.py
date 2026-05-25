from contextlib import contextmanager

from testcontainers.postgres import PostgresContainer


@contextmanager
def get_postgres_container() -> PostgresContainer:
    try:
        container = PostgresContainer("postgres:15")
        container.start()
        yield container
    except Exception as e:
        raise Exception("Unable to create postgres test container")
    finally:
        container.stop()
