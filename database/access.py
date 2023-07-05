from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(engine)

