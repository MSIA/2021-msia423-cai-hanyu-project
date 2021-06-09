# MSiA423 Repository -- Hanyu Cai

Hanyu Cai

QA: Dian Yu



**Vision**:

As one of the most favorite snacks in the United States, the chocolate bar was consumed in an impressive amount in the United States, not to mention that the global chocolate industry worth 100 billion dollars. There are around 2000+ chocolate bar products, with different combinations of the cocoa bean, cocoa percentage, ingredients, and flavor, in the United States market. Thus, when chocolate manufacturers start to expand their market, or when consumers want to explore new chocolate bar products, it can be hard to choose the right product from such a great variety of chocolate bars. This application aims to recommend users chocolate bars and give a predicted rating for the taste of the chocolate bar combination they enter.

**Mission**:

Users would be prompted to choose their preferences over chocolate bars – such as the chocolate bean type, cocoa percentage, and ingredients of chocolate bars. Based on the information users provided, the application would give user 10 recommendations about the possible chocolate bar according to their preferences. The application would use a k-means clustering for recommendation, information like chocolate bar bean name, ratings, cocoa percentage, and flavors would also be given for the products recommended.

Datasets: https://www.kaggle.com/soroushghaderi/chocolate-bar-2020 The dataset contains information from 2006 to 2020 in 66 countries about over 1700 chocolate reviews and tastes, chocolate company name, country of the chocolate bean, etc.

**Metric**:

1.Machine learning performance metric:

Since the recommendation system is unsupervised learning, there is no right or wrong about the recommendation. To ensure that the chocolate bar recommender successfully differentiate and identify similar products. I use silhouette score to measure my k-means clustering recommendation model. A silhouette score > 0.4 would mean that the each product in the k-means clustering model is well matched to its own cluster and is different from products in other clusters.

2.Business metric:

After the application is launched, I would measure the number of clicks to my websites. By measuring the average click number per week, I could infer the popularity of my application -- a higher average cliclk number means the application is popular. Also, I plan to give satisfaction survey to users. The satisfaction survey would ask users to rate the application and give feedback on whether recommendations given by the website is effective.


## Proj Template 
<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Build docker image](#1-build-docker-image)
      - [Add environment variables to access s3](#add-environment-variables-to-access-s3)
      - [Uploading raw data to s3](#uploading-raw-data-to-s3)
  * [2. Upload data to S3 bucket](#2-upload-data-to-s3-bucket)
  * [3. Create MYSQL database](#3-create-mysql-database)
     - [Create database on local](#create-database-on-local)
     - [Create database on RDS](#create-database-on-rds)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│   ├── chocolate_data/               <- The raw data folder
│   ├── clean_data.csv                <- The cleaned data after processing
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│   ├── test_s3.py                    <- Test the s3.py functioning
│   ├── test_clean_data.py            <- Test the clean_data.py functioning
│   ├── test_modeling.py              <- Test the modeling.py functioning
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
├── pipeline.sh                       <- shell commands to run model pipeline 
├── connect_mysqldb.sh                <- shell commands to connect mysql database
├── connect_mysqldb.sh                <- shell commands to connect mysql database
├── connect_mysqldb.sh                <- shell commands to connect mysql database
```

## Running the app

**Connect to Northwestern VPN before running the following commands**

### 1. Build docker image 

`docker build -f Dockerfile -t chocolate .`

### 2. Upload data to S3 bucket

#### Add environment variables to access s3
```
export AWS_ACCESS_KEY_ID="AWS KEY ID"
export AWS_SECRET_ACCESS_KEY="AWS KEY"
```

The raw data is located at  data/chocolate_data/chocolate.csv

#### Uploading raw data to s3 
`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY chocolate run.py upload --s3path s3://2021-msia423-cai-hanyu/chocolate.csv --local_path data/chocolate_data/chocolate.csv`

#### Downloading data from s3
`docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY chocolate run.py download --s3path s3://2021-msia423-cai-hanyu/chocolate.csv --local_path data/chocolate_data/chocolate.csv`

### 3. Create MYSQL database

#### Create database on local

`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -it chocolate run.py create_db`

To specify the enginee string, using: 

`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -it chocolate run.py create_db --engine_string <MY ENGINE STRING>`

(Note: you may also specify enginee sting by setting environment variable SQLALCHEMY_DATABASE_URI)
 
#### Create database on RDS 
Specify the environment variables in .mysqlconfig file (use "vi .mysqlconfig" to open the file):

```
export MYSQL_USER="RDS Username"
export MYSQL_PASSWORD="RDS Password"
export MYSQL_PORT="3306"
export MYSQL_DB="msia423_db"
export MYSQL_HOST="MY HOST"
```

Set up the environment variables

`source .mysqlconfig`

Run the following command to initiate database with name "msia423_db" & create table named "chocolates" on RDS

`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e MYSQL_DB -e MYSQL_HOST chocolate run.py create_db`

### 4.Run Model Pipeline
Please remember to export environment variables before running model pipeline (following similar procedure for step 2 and 3):

```
export AWS_ACCESS_KEY_ID=<Your Access Key ID>
export AWS_SECRET_ACCESS_KEY=<Your Secret Key ID>
export MYSQL_USER="RDS Username"
export MYSQL_PASSWORD="RDS Password"
export MYSQL_PORT="3306"
export MYSQL_DB="msia423_db"
export MYSQL_HOST="MY HOST"
```

Build docker image

`docker build -f Dockerfile_sh -t chocolate_sh .`

Run model pipeline via 'pipeline.sh'

`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e MYSQL_DB -e MYSQL_HOST chocolate_sh pipeline.sh`

### 5.Upload the chocolate bar records to RDS database for recommendation

**(Note: Please first check if data alreay exists in RDS database. If so, please DON'T re-upload data, which may causes duplicate issues in flask app.)**

The following command would upload the pre-processed dataset to RDS for prediction use:

`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e MYSQL_DB -e MYSQL_HOST chocolate run.py store_rds --file_path data/clean_data.csv`

Connect to MYSQL database:

`sh connect_mysqldb.sh`

Use the following commands to check if table is successfully added to RDS database:
```
use msia423_db;
show columns from chocolates;
```

### 6.Launch the Web Application
Build a new docker image for web application
`docker build -f app/Dockerfile -t chocolate_application`

Access by using environment variables set up in .mysqlconfig:
`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e MYSQL_DB -e MYSQL_HOST -p 5000:5000 -it chocolate_application`

Access by using SQLALCHEMY_DATABASE_URI:
`docker run --mount type=bind,source="$(pwd)"/data,target=/app/data -e SQLALCHEMY_DATABASE_URI -p 5000:5000 -it chocolate_application`

You may access the website at http://0.0.0.0:5000/ now

### 7. Test s3.py 

Build docker image
`docker build -f Dockerfile_sh -t chocolate_sh .`

Run the following command to test in docker container chocolate:
`docker run chocolate_sh test.sh`
