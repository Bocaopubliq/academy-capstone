from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as pf
from pyspark.sql.types import DateType
import boto3
import json

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

def get_spark_session(name: str = None) -> SparkSession:
    return (
        SparkSession.builder
        .config(
            "spark.jars.packages",
            ",".join(
                [
                    "org.apache.hadoop:hadoop-aws:3.1.2",
                    "net.snowflake:spark-snowflake_2.12:2.12.0-spark_3.4",
                    "net.snowflake:snowflake-jdbc:3.14.1",
                ]
            ),
        )
        .config(
            "fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
        )
        .getOrCreate()
    )



def clean_data(df):
    #flatten columns
    df = df.withColumn("latitude", pf.col("coordinates.latitude")) \
       .withColumn("longitude", pf.col("coordinates.longitude")) \
       .withColumn("local_date", pf.col("date.local")) \
       .withColumn("utc_date", pf.col("date.utc")) \
       .drop("coordinates") \
       .drop("date")
    df = df.withColumn("local_date", pf.col("local_date").cast(DateType())).withColumn("utc_date", pf.col("utc_date").cast(DateType()))
    return df

def get_snowflake_credentials():
    # Define the AWS region where Secrets Manager is located
    region_name = 'eu-west-1'

    # Define the name of the secret containing Snowflake credentials
    secret_name = 'snowflake/capstone/config'

    # Create a Secrets Manager client
    client = boto3.client(service_name='secretsmanager', region_name=region_name)

    # Retrieve the secret value
    # response = client.get_secret_value(SecretId='arn:aws:secretsmanager:eu-west-1:338791806049:secret:snowflake/capstone/config-dGwyDK')
    response = client.get_secret_value(SecretId=secret_name)

    # Parse and return the Snowflake credentials
    secret_dict = json.loads(response['SecretString'])

    return secret_dict


def snowflake_config():
    credentials = get_snowflake_credentials()
    print(credentials)
    return {
        "sfURL": credentials["URL"],
        "sfUser": credentials["USER_NAME"],
        "sfPassword": credentials["PASSWORD"],
        "sfDatabase": credentials["DATABASE"],
        "sfWarehouse": credentials["WAREHOUSE"],
        "sfRole": credentials["ROLE"],
        "sfSchema": 'BO',
    }

def load_and_write():
    
    spark = get_spark_session()

    df = spark.read.json(f"s3a://dataminded-academy-capstone-resources/raw/open_aq/")
    final = clean_data(df)
    final.write.format(SNOWFLAKE_SOURCE_NAME).options(**snowflake_config()).option(
        "dbtable", "open_aq"
    ).mode("overwrite").save()
    
    

if __name__ == "__main__":
    load_and_write()
