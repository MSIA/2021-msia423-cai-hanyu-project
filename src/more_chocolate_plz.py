import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
Base = declarative_base()


class Chocolates(Base):

    """
    Create a data model for the database to load chocolate bars rating data
    """

    __tablename__ = "chocolates"
    index = Column(Integer, primary_key=True)
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

    data = pd.read_csv(file_path)

    for i in range(len(data)):
        each_row = Chocolates(company=str(data['company'][i]),
                              specific_bean_origin_or_bar_name
                              =str(data['specific_bean_origin_or_bar_name'][i]),
                              cocoa_percent=float(data['cocoa_percent'][i]),
                              rating=float(data['rating'][i]),
                              beans=int(data['beans'][i]),
                              cocoa_butter=int(data['cocoa_butter'][i]),
                              vanilla=int(data['vanilla'][i]),
                              lecithin=int(data['lecithin'][i]),
                              salt=int(data['salt'][i]),
                              sugar=int(data['sugar'][i]),
                              sweetener_without_sugar=int(data['sweetener_without_sugar'][i]),
                              first_taste=str(data['first_taste'][i]),
                              second_taste=str(data['second_taste'][i]))

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
    except Exception as errors:
        logger.error(errors)
    finally:
        session.close()
