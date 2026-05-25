from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base


def get_sessionmaker(url: str) -> sessionmaker:
    engine = create_engine(url)

    session_maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    return session_maker

def override_get_db():
    db = _test_session_maker()
    try:
        yield db
    finally:
        db.close()