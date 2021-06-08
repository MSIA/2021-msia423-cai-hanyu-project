import logging.config
import os

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
Base = declarative_base()


class Chocolates(Base):

    """
    Create a data model for the database to load chocolate bars rating data
    """

    __tablename__ = "chocolates"
    chocolate_key = Column(Integer, primary_key=True)
    index = Column(Integer, unique=False, nullable=False)
    company = Column(String(25), unique=False, nullable=False)
    specific_bean_origin_or_bar_name = Column(String(50), unique=False, nullable=False)
    cocoa_percent = Column(Float(), unique=False, nullable=False)
    rating = Column(Float(), unique=False, nullable=False)
    beans = Column(String(25), unique=False, nullable=False)
    cocoa_butter = Column(String(25), unique=False, nullable=False)
    vanilla = Column(String(25), unique=False, nullable=False)
    lecithin = Column(String(25), unique=False, nullable=False)
    salt = Column(String(25), unique=False, nullable=False)
    sugar = Column(String(25), unique=False, nullable=False)
    sweetener_without_sugar = Column(String(25), unique=False, nullable=False)
    first_taste = Column(String(25), unique=False, nullable=False)
    second_taste = Column(String(25), unique=False, nullable=False)

    def __repr__(self):
        return "<Chocolate Bar No. %i>" % self.index


def create_db(engine_string):
    """
    Create database from provided engine string

    Args:
        engine_string (str): Engine string

    Returns: 
        None
    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info(engine)
    logger.info("Database created.")


def add_rows(file_path, session):
    """Add rows of chocolate bar records into the RDS database

    Args:
        file_path (str): local recommendation table to be written into database
        session (str): get session from SQLAlchemy connection string

    Returns:
        None
    """

    df = pd.read_csv(file_path)

    for i in range(len(df)):
        each_row = Chocolates(index=int(df['index'][i]),
                             company=str(df['company'][i]),
                             specific_bean_origin_or_bar_name=str(df['specific_bean_origin_or_bar_name'][i]),
                             cocoa_percent=float(df['cocoa_percent'][i]),
                             rating=float(df['rating'][i]),
                             beans=int(df['beans'][i]),
                             cocoa_butter=int(df['cocoa_butter'][i]),
                             vanilla=int(df['vanilla'][i]),
                             lecithin=int(df['lecithin'][i]),
                             salt=int(df['salt'][i]),
                             sugar=int(df['sugar'][i]),
                             sweetener_without_sugar=int(df['sweetener_without_sugar'][i]),
                             first_taste = str(df['first_taste'][i]),
                             second_taste=str(df['second_taste'][i]))

        session.add(each_row)

    session.commit()
    logger.debug("Session commit complete")


def upload_to_rds(file_path, engine_string):
    """ Create database in RDS for the chocolate bar table 

    Args:
        file_path (str): input file path
        engine_string (str): engine string for the RDS database
        
    Returns:
        None
    """

    # generate engine string
    engine_string = sqlalchemy.create_engine(engine_string)
    logger.info(engine_string)

    Session = sessionmaker(bind=engine_string)
    session = Session()

    # write records into table
    try:
        # write records into table
        add_rows(file_path, session)
        logger.info("Database created successfully with all records added")
    except Exception as e:
        logger.error(e)
    finally:
        session.close()
