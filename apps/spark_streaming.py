from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType
from pyspark.sql.functions import from_json,col,sum,avg,max,count, window, expr
spark = SparkSession.builder\
    .appName("trip-app-1")\
    .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "demo") \
  .load()


df1 = df.selectExpr("CAST(value AS STRING)", "timestamp")\
        .select(col("value"), col("timestamp"))
        #.groupBy("value").count()
# df2 = df.selectExpr("CAST(value AS STRING)", "timestamp")\
#         .select(col("value"), col("timestamp"))\
#         .withWatermark("timestamp", "1 minutes")\
#         .groupBy("value", "timestamp")\
#         .agg(count("value"))
#         #.groupBy(col("value"), "timestamp").count()

df2 = df.selectExpr("CAST(value AS STRING)", "timestamp")\
        .select(col("value"), col("timestamp"))\
        .withWatermark("timestamp", "10 seconds")\
        .groupBy(
            window("timestamp", "10 seconds"),
            #"value"
        )\
        .agg(count("value"))\
        .select(col("window"), col("count(value)"), expr("window.start"), expr("window.end"))\
        #.groupBy(col("value"), "timestamp").count()
# data_1 = df1.writeStream\
#     .format("console")\
#     .outputMode("complete")\
#     .trigger(processingTime="10 second")\
#     .start()

data_2 = df2.writeStream\
    .format("console")\
    .outputMode("append")\
    .trigger(processingTime="30 second")\
    .option("truncate", False)\
    .start()

#data_1.awaitTermination(10000)

# df.printSchema()
# data=df.writeStream\
#     .format("console")\
#     .outputMode("append")\
#     .trigger(processingTime="30 second")\
#     .start()
#data.awaitTermination()

data_1 = df1.writeStream\
    .format("console")\
    .outputMode("append")\
    .trigger(processingTime="30 second")\
    .option("truncate", False)\
    .start()
data_1.awaitTermination(10000)
data_2.awaitTermination(10000)
