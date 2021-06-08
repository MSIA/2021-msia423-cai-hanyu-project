#!/usr/bin/env bash

# Download data from S3 bucket
python3 run.py upload --s3path s3://2021-msia423-cai-hanyu/chocolate.csv --local_path data/chocolate_data/chocolate.csv

# Generate k means clustering model and evaluate performances
python3 run.py run_modeling --local_path data/chocolate_data/chocolate.csv --config config/config.yaml

# Upload cleaned table to RDS
python3 run.py store_rds --file_path data/clean_data.csv 