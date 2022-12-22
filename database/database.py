import os

from sqlalchemy.future import create_engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from database.models import Base


class Database:
    def __init__(self, objects) -> None:
        self.objects = objects

    def commit_data(self) -> None:
        for item_list in self.objects:
            session.add_all(item_list)
        session.commit()
        session.close()


load_dotenv()
database_uri = os.environ['DATABASE_URI']

engine = create_engine(database_uri, echo=True)
session = Session(bind=engine)
Base.metadata.create_all(engine)
