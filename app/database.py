from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Establish a link for connection
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Generate an engine to connect SQLalchemy to postgresql (link above)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

#Nothat you are connected, you need to manage sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Help us talk to the database
Base = declarative_base()

# Dependency
#Gets called anytime we get a request to our API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Connect using Psycopg2
# import psycopg2
# # Gives you column name as well as values
# from psycopg2.extras import RealDictCursor
# # use time to add a small delay incase we need to reconnect
# import time
# # Connect to an existing database - using psycopg
# # also continue to try everytime these is a disconnection
# while True:    
#     try:
#         conn = psycopg2.connect(host ='localhost', database='fastapi', 
#         user='postgres', password='#NaimData', cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print('Error: ', error)
#         time.sleep(2)