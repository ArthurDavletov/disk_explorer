import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Directory(Base):
    __tablename__ = "directories"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    n_dirs = Column(Integer)
    n_files = Column(Integer)
    last_changed = Column(Numeric)


if __name__ == '__main__':
    engine = create_engine("sqlite://directories.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
