from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# SQLALCHEMY_DATABASE_URL_CONNECT = "postgresql+psycopg2://postgres:postgres@192.168.0.19:4509/authentication"
SQLALCHEMY_DATABASE_URL_CONNECT = "postgresql+psycopg2://postgres:postgres@192.168.0.19:4509/aq_authentication?options=-csearch_path=Rolemaster"




engineconnect = create_engine(SQLALCHEMY_DATABASE_URL_CONNECT, pool_pre_ping=True)
SessionLocalConnect = sessionmaker(autocommit=False, autoflush=False, bind=engineconnect)
Base = declarative_base()

def get_db():
    db = SessionLocalConnect()
    try:
        yield db
    finally:
        db.close()
