from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format
from datetime import datetime, date
import os
import pandas as pd
from pyspark.sql import Row

os.environ['PYSPARK_PYTHON'] = "./environment/bin/python"

def init_spark():
  sql = SparkSession.builder\
    .appName("app-01")\
    .master("spark://localhost:7077")\
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.archives","pyspark_venv.tar.gz#environment")\
    .getOrCreate()
  sc = sql.sparkContext
  sc.setLogLevel('WARN')

  return sql,sc

def main():
  sql,sc = init_spark()
  df = sql.createDataFrame([
      Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
      Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
      Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
  ], schema='a long, b double, c string, d date, e timestamp')

  df.printSchema()
  # file = "/opt/spark-data/B63-2011-04-03_2011-05-03.csv"
  # df = sql.read.load(file,format = "csv", inferSchema="true", sep=",", header="true"
  #     )\
  #     .withColumn("report_hour",date_format(col("timestamp"),"yyyy-MM-dd HH:00:00")) \
  #     .withColumn("report_date",date_format(col("timestamp"),"yyyy-MM-dd"))
  
  # df.printSchema()

if __name__ == '__main__':
  main()