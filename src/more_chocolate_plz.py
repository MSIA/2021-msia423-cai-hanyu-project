import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Chocolates(Base):
    """Create a data model for the database to load chocolate bars rating data"""

    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    ref = Column(Integer(), nullable=False)
    company = Column(String(100), unique=False, nullable=False)
    country_of_bean_origin = Column(String(25), unique=False, nullable=False)
    cocoa_percent = Column(Float(), nullable=False)
    rating = Column(Float(), nullable=False)
    counts_of_ingredients = Column(Integer(), nullable=False)
    beans = Column(String(25), unique=False, nullable=False)
    cocoa_butter = Column(String(25), unique=False, nullable=False)
    vanilla = Column(String(25), unique=False, nullable=False)
    lecithin = Column(String(25), unique=False, nullable=False)
    salt = Column(String(25), unique=False, nullable=False)
    sugar = Column(String(25), unique=False, nullable=False)
    sweetener_without_sugar = Column(String(25), unique=False, nullable=False)
    first_taste = Column(String(25), unique=False, nullable=False)
    second_taste = Column(String(25), unique=False, nullable=True)
    third_taste = Column(String(25), unique=False, nullable=True)
    fourth_taste = Column(String(25), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Chocolate Bar Ref Number %r>' % ref


def create_db(engine_string: str):
    """
    Create database from provided engine string

    Args:
        engine_string: str - Engine string

    Returns: None
    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")

def delete_db(engine_string: str):
    """
    Delete database from provided engine string.
    
    Args:
        engine_string: str - Engine string
        
    Returns: None
    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.drop_all(engine)
    logger.info("Database deleted")
    
class ChocolateManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self):
        """Closes session

        Returns: None

        """
        self.session.close()

    def add_chocolate(self, id, ref, company, country_of_bean_origin, cocoa_percent, rating,
                      counts_of_ingredients, beans, cocoa_butter, vanilla, lecithin, salt, sugar,
                      sweetener_wirhout_sugar,first_taste,second_taste,third_taste,fourth_taste):
        
        """Seeds an existing database with additional chocolate bars."""

        session = self.session
        bar = Chocolates(id=id, ref=ref, company=company, country_of_bean_origin=country_of_bean_origin,
                           cocoa_percent=cocoa_percent, rating=rating,counts_of_ingredients=counts_of_ingredients,
                           beans=beans, cocoa_butter=cocoa_butter, vanilla=vanilla, lecithin=lecithin, salt=salt,
                           sugar=sugar,sweetener_wirhout_sugar=sweetener_wirhout_sugar,first_taste=first_taste,
                           second_taste=second_taste,third_taste=third_taste,fourth_taste=fourth_taste)
        session.add(bar)
        session.commit()
        logger.info("chocolate bar ref number %s from company %s added to database", ref, company)
