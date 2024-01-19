from db.utils import Base, engine
from dotenv import load_dotenv

import os
from db.Incident import *

load_dotenv()

if __name__ == "__main__":
    print("Creating DB")
    print("Connection string")
    print(
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:5432/{os.getenv('DATABASE_NAME')}"
    )
    Base.metadata.create_all(engine)
