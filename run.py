import argparse
import logging.config
import pkg_resources

import yaml

from src.more_chocolate_plz import create_db, upload_to_rds
from src.s3 import upload_file_to_s3,download_file_from_s3
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.clean_data import clean
from src.modeling import get_userinput, generate_kmeans, predict_user_input

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
    sb_create.add_argument('--config', default='config/config.yaml', help='Path to configuration file')

    # Sub-parser for uploading data to s3
    sb_upload = subparsers.add_parser("upload", help="Upload raw data to s3")
    sb_upload.add_argument("--s3path", default="s3://2021-msia423-cai-hanyu/chocolate.csv", help="S3 data path")
    sb_upload.add_argument("--local_path", default="data/chocolate_data/chocolate.csv", help="The local path")
    sb_upload.add_argument('--config', default='config/config.yaml', help='Path to configuration file')

    # Sub-parser for downloading data to s3
    sb_download = subparsers.add_parser("download", help="Download raw data to s3")
    sb_download.add_argument("--s3path", default="s3://2021-msia423-cai-hanyu/chocolate.csv", help="S3 data path")
    sb_download.add_argument("--local_path", default="data/chocolate_data/chocolate.csv", help="The local path")
    sb_download.add_argument('--config', default='config/config.yaml', help='Path to configuration file')

    # Sub-parser for modeling from csv
    sb_csv_modeling = subparsers.add_parser("csv_modeling", help="Modeling by running local csv file")
    sb_csv_modeling.add_argument("--local_path", default="data/chocolate_data/chocolate.csv", help="The local path")
    sb_csv_modeling.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    sb_csv_modeling.add_argument("--cocoa_percent", default='72.0', help="cocoa percentage for chocolate bar added")
    sb_csv_modeling.add_argument("--rating", default='3.75', help="rating for chocolate bar added")
    sb_csv_modeling.add_argument("--beans", default='Yes', help="beans for chocolate bar added")
    sb_csv_modeling.add_argument("--cocoa_butter", default='Yes', help="if cocoa butter is in the chocolate bar added")
    sb_csv_modeling.add_argument("--vanilla", default='No', help="if vanilla is in the chocolate bar added")
    sb_csv_modeling.add_argument("--lecithin",  default='Yes', help="if lecithin is in the chocolate bar added")
    sb_csv_modeling.add_argument("--salt",  default='No', help="if salt is in the chocolate bar added")
    sb_csv_modeling.add_argument("--sugar",  default='No', help="if sugar is in the chocolate bar added")
    sb_csv_modeling.add_argument("--sweetener_without_sugar", default='Yes', help="if the chocolate bar has sweetener "
                                                                              "without sugar")
    # Store generated recommendations into RDS
    sb_rds = subparsers.add_parser("store_rds", description="store cleaned table into RDS database")
    sb_rds.add_argument('--file_path', default='data/clean_data.csv', help='path of clean data')
    sb_rds.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    sb_rds.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sb_used = args.subparser_name

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
    elif sb_used == "csv_modeling":
        #clean data
        df = clean(args.local_path, **config['clean_data']['clean'])
        # user insert value
        input_value = get_userinput(args.cocoa_percent, args.rating, args.beans, args.cocoa_butter, args.vanilla,
                                    args.lecithin, args.salt, args.sugar, args.sweetener_without_sugar, **config['modeling']['get_userinput'])
        #generate k means model and save to joblib
        generate_kmeans(df, **config['modeling']['generate_kmeans'])
        #get prediction result
        predict_user_input(df, input_value, **config['modeling']['predict_user_input'])
    elif sb_used == "store_rds":
        upload_to_rds(args.file_path,args.engine_string)
    else:
        parser.print_help()



