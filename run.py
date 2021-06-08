import argparse
import logging.config
import pkg_resources

import yaml

from src.more_chocolate_plz import create_db, upload_to_rds
from src.s3 import upload_file_to_s3, download_file_from_s3
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.clean_data import clean, standardization
from src.modeling import generate_kmeans, model_evaluation

logging.config.fileConfig(pkg_resources.resource_filename(__name__, "config/logging/local.conf"),
                          disable_existing_loggers=False)
logger = logging.getLogger("chocolate bars")

if __name__ == '__main__':

    # Add parsers for both creating a database and adding chocolates to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for uploading data to s3
    sb_upload = subparsers.add_parser("upload", help="Upload raw data to s3")
    sb_upload.add_argument("--s3path", default=None, help="S3 data path")
    sb_upload.add_argument("--local_path", default=None, help="The local path")

    # Sub-parser for downloading data to s3
    sb_download = subparsers.add_parser("download", help="Download raw data to s3")
    sb_download.add_argument("--s3path", default=None, help="S3 data path")
    sb_download.add_argument("--local_path", default=None, help="The local path")

    # Sub-parser for modeling from csv
    sb_run_modeling = subparsers.add_parser("run_modeling", help="Modeling and output recommendations to user")
    sb_run_modeling.add_argument("--local_path", default=None, help="The local path")
    sb_run_modeling.add_argument('--config', default=None, help='Path to configuration file')

    # Store generated recommendations into RDS
    sb_rds = subparsers.add_parser("store_rds", help="store cleaned table into RDS database")
    sb_rds.add_argument('--file_path', default=None, help='path of clean data')
    sb_rds.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sb_used = args.subparser_name

    if  sb_used == "run_modeling":
        # Load configuration file for parameters and tmo path
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logger.info("Configuration file loaded from %s" % args.config)

    if sb_used == "upload":
        upload_file_to_s3(args.local_path, args.s3path)
    elif sb_used == "download":
        download_file_from_s3(args.local_path, args.s3path)
    elif sb_used == "create_db":
        create_db(args.engine_string)
    elif sb_used == "run_modeling":
        # clean data
        df = clean(args.local_path, **config['clean_data']['clean'])
        # standardization
        scale_df = standardization(df, **config['clean_data']['standardization'])
        # generate k means model and save to joblib
        model = generate_kmeans(scale_df, **config['modeling']['generate_kmeans'])
        # model evaluation
        model_evaluation(scale_df, model, **config['modeling']['model_evaluation'])
    elif sb_used == "store_rds":
        upload_to_rds(args.file_path, args.engine_string)
    else:
        parser.print_help()




