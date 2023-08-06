# functions for working with activity stream data in Spark

from pyspark.sql import SparkSession


spark = SparkSession.builder.getOrCreate()


def pull_tiles_data(sql_query, pw):
    """
    provide SQL query, will return spark df of results
    """

    TEMPDIR = "s3n://mozilla-databricks-telemetry-test/tiles-redshift/_temp"
    JDBC_URL = ("jdbc:postgresql://databricks-tiles-redshift.data.mozaws.net" +
                ":5432/tiles?user=databricks" +
                "&password=%s" +
                "&ssl=true&sslMode=verify-ca" % pw)

    df = spark.read.format("com.databricks.spark.redshift")\
                   .option("forward_spark_s3_credentials", True)\
                   .option("url", JDBC_URL).option("tempdir", TEMPDIR)\
                   .option("query", sql_query)\
                   .load()
    return df
