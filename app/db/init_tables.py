from app.db.db import engine, Base
from app.db import models


def init_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_tables()
    print("Tables created")
