import logging.config
import traceback

import pandas as pd
import yaml
from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

from src.modeling import get_userinput, predict_user_input
from src.more_chocolate_plz import Chocolates

# export FLASK_DEBUG=1
# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database
db = SQLAlchemy(app)

# Connect to RDS or local database and query all data
logger.info('Connecting to %s', app.config['SQLALCHEMY_DATABASE_URI'])
recs = db.session.query(Chocolates)


# load config yaml
try:
    with open(app.config['CONFIGS'], "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded from %s", app.config['CONFIGS'])
except FileNotFoundError:
    logger.error("Configuration file %s is not found", app.config['CONFIGS'])


@app.route('/')
def index():
    """  Create view into index page that collects user input data
    Returns: rendered html template
    """
    try:
        logger.debug("Index page accessed")
        return render_template('index.html', booleans=app.config['BOOLS'])
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """  The submission page that list out recommendation table for user
    Returns: rendered html template
    """
    try:
        logger.debug("submmission page accessed")
        # get data from rds 
        data = pd.read_sql(recs.statement, recs.session.bind)
        # user insert value
        input_value = get_userinput(request.form["cocoa_percent"], request.form["rating"],
                                    request.form["beans"], request.form["cocoa_butter"],
                                    request.form["vanilla"], request.form["lecithin"],
                                    request.form["salt"], request.form["sugar"],
                                    request.form["sweetener_without_sugar"],
                                    **config['modeling']['get_userinput'])
        # get prediction result
        recommendation = predict_user_input(data, input_value, **config['modeling']['predict_user_input'])
        return render_template('submit.html', rec=recommendation.values)
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')
    

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
