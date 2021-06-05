import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for
import yaml

from flask_sqlalchemy import SQLAlchemy
from src.more_chocolate_plz import Chocolates
from src.clean_data import clean
from src.modeling import get_userinput, generate_kmeans, predict_user_input

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
#logger.info('Connecting to '+ app.config['SQLALCHEMY_DATABASE_URI'])
#recs = db.session.query(Chocolates).all()

BOOLS = ['Yes','No']

#load config yaml
with open('config/config.yaml', "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded from %s" % 'config/config.yaml')

@app.route('/')
def index():
    """  Create view into index page that collects user input data
    Returns: rendered html template
    """
    try:
        #applications = application_manager.session.query(Application).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html',booleans = BOOLS)
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    try:
        logger.debug("submmission page accessed")
        #clean data
        df = clean('data/chocolate_data/chocolate.csv', **config['clean_data']['clean'])
        # user insert value
        input_value = get_userinput(request.form["cocoa_percent"], request.form["rating"], request.form["beans"], request.form["cocoa_butter"], 
                                request.form["vanilla"],request.form["lecithin"],request.form["salt"],request.form["sugar"],
                                request.form["sweetener_without_sugar"], **config['modeling']['get_userinput'])
        #get prediction result
        recommendation = predict_user_input(df, input_value, **config['modeling']['predict_user_input'])
        print(recommendation)
        return render_template('submit.html',rec = recommendation.values)
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')
    

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
