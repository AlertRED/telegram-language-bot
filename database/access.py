from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://", echo=True)


def session_commit(*args):
    with Session(engine) as session:
        try:
            session.add_all(args)
        except Exception:
            session.rollback()
        finally:
            session.commit()
