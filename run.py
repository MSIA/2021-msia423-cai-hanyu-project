import argparse
import logging.config
import pkg_resources

from src.more_chocolate_plz import ChocolateManager, create_db
from src.s3 import upload_file_to_s3
from config.flaskconfig import SQLALCHEMY_DATABASE_URI


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
    sb_upload.add_argument("--s3path", default="s3://2021-msia423-cai-hanyu/chocolate.csv", help="S3 data path")
    sb_upload.add_argument("--local_path", default="data/chocolate_data/chocolate.csv", help="The local path")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--ref", help="Reference number for chocolate bar added")
    sb_ingest.add_argument("--company",  help="company for chocolate bar added")
    sb_ingest.add_argument("--country_of_bean_origin", help="country for the chocolate bean of the chocolate bar added")
    sb_ingest.add_argument("--cocoa_percent", help="cocoa percentage for chocolate bar added")
    sb_ingest.add_argument("--rating", help="rating for chocolate bar added")
    sb_ingest.add_argument("--counts_of_ingredients",help="counts of ingredients for chocolate bar added")
    sb_ingest.add_argument("--beans", help="beans for chocolate bar added")
    sb_ingest.add_argument("--cocoa_butter",help="if cocoa butter is in the chocolate bar added")
    sb_ingest.add_argument("--vanilla",help="if vanilla is in the chocolate bar added")
    sb_ingest.add_argument("--lecithin",help="if lecithin is in the chocolate bar added")
    sb_ingest.add_argument("--salt",help="if salt is in the chocolate bar added")
    sb_ingest.add_argument("--sugar",help="if sugar is in the chocolate bar added")
    sb_ingest.add_argument("--sweetener_without_sugar",help="if sweetener_wirhout_sugar is in the chocolate bar added")
    sb_ingest.add_argument("--first_taste",help="first taste of chocolate bar added")
    sb_ingest.add_argument("--second_taste",help="second taste of chocolate bar added")
    sb_ingest.add_argument("--third_taste",help="third taste of chocolate bar added")
    sb_ingest.add_argument("--fourth_taste",help="fourth taste of chocolate bar added")

    args = parser.parse_args()
    sb_used = args.subparser_name
    if sb_used == "upload":
        upload_file_to_s3(args.local_path, args.s3path)
    elif sb_used == "create_db":
        create_db(args.engine_string)
    elif sb_used == "ingest":
        tm = ChocolateManager(engine_string=args.engine_string)
        tm.add_chocolate(args.ref, args.company, args.country_of_bean_origin, args.cocoa_percent, args.rating,
                         args.counts_of_ingredients, args.beans, args.cocoa_butter, args.vanilla, args.lecithin,
                         args.salt, args.sugar, args.sweetener_without_sugar, args.first_taste, args.second_taste,
                         args.third_taste, args.fourth_taste)
        tm.close()
    else:
        parser.print_help()



