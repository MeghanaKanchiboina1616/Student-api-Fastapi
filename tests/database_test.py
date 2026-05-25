from testcontainers.postgres import PostgresContainer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base

# Start PostgreSQL container
postgres = PostgresContainer("postgres:15")
postgres.start()

# Get temporary DB URL
DATABASE_URL = postgres.get_connection_url()

# Create engine
engine = create_engine(DATABASE_URL)

# Session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create tables
Base.metadata.create_all(bind=engine)


# Override DB dependency
def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


# Cleanup
#def stop_container():
   # postgres.stop()