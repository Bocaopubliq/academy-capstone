from pyspark import SparkConf
from pyspark.sql import SparkSession

config = {
    "spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.1.2",
    "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
}
conf = SparkConf().setAll(config.items())
spark = SparkSession.builder.config(conf=conf).getOrCreate()

df = spark.read.csv(f"s3://dataminded-academy-capstone-resources/raw/open_aq/", header=True).cache()
df.show()
