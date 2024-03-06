from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format
from datetime import datetime, date
import os
from pyspark.sql import Row

os.environ['PYSPARK_PYTHON'] = "./environment/pyspark_venv.pex"

def init_spark():
    sql = SparkSession.builder \
        .appName("app-01") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.archives", "app_venv.pex#environment") \
        .getOrCreate()
    sc = sql.sparkContext
    sc.setLogLevel('WARN')

    return sql, sc


def main():
    sql, _ = init_spark()
    df = sql.createDataFrame([
        Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
        Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
        Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
    ], schema='a long, b double, c string, d date, e timestamp')

    df.printSchema()
    sql.stop()


if __name__ == '__main__':
    main()
