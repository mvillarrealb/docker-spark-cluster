from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.functions import split, regexp_extract, sum,avg, min, max, mean, count, col, asc,desc, to_timestamp, to_date
spark = SparkSession.builder.appName('kdd4').getOrCreate()
spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
base_df = spark.read.text(
    '/opt/spark-data/access.log')
print(base_df.schema)


split_df = base_df.select(
                        'value',
                        regexp_extract('value', r'^([^\s]+)\s', 1).alias('host'),
                        regexp_extract('value', r'^([^\s]+)\s([^\s]+)', 2).alias('available_request'),
                        regexp_extract('value', r'^([^\s]+)\s([^\s]+)\s([^\s]+)\s', 3).alias('user'),
                        regexp_extract('value', r'^.*\[(\d\d/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]\s', 1).alias('timestamp'),
                        # regexp_extract('value', r'^.*"(\w+\s+([^\s]+)\s+HTTP[^\s]+)"\s', 1).alias('path'),
                        regexp_extract('value', r'[^"]+"([^"]+)"', 1).alias('path'),
                        regexp_extract('value', r'^.*"\s+(\d+)\s', 1).cast('integer').alias('status'),
                        regexp_extract('value', r'^.*\s+(\d+)\s', 1).cast('integer').alias('content_size'),
                        regexp_extract('value', r'^.*\s+(\d+)\s"([^"]+)"\s', 2).alias('referer'),
                        regexp_extract('value', r'^.*\s+(\d+)\s"([^"]+)"\s"([^"]+)"', 3).alias('agent')
                    ).select(
                        'value',
                        'host',
                        'available_request',
                        'user',
                        'timestamp',
                        to_timestamp('timestamp', "dd/MMM/yyyy:HH:mm:ss ZZZZ").alias("utc_ts"),
                        to_date(to_timestamp('timestamp', "dd/MMM/yyyy")).alias("utc_dt"),
                        'path',
                        regexp_extract('path', r'([^\s]+)\s', 1).alias('method'),
                        regexp_extract('path', r'([^\s]+)\s([^\s]+)\s', 2).alias('endpoint'),
                        regexp_extract('path', r'([^\s]+)\s([^\s]+)\s(HTTP[^\s]+)', 3).alias('http_version'),
                        'status',
                        'content_size',
                        'referer',
                        'agent'
                    )
#  split_df.filter(split_df.agent != "-").show(30,truncate=False)
# df.where(col("dt_mvmt").isNotNull())

# split_df.show(10, truncate=False)
# split_df.take(10)

# rows = query1_df.count()
# print(f"DataFrame Rows count : {rows}")
#split_df.filter(split_df.user != '-').show(30,truncate=False)

# thong ke theo host
# query1_df = split_df.groupby('host')\
#     .agg(count('*').alias('count_host'))\
#     .sort(col('count_host').desc())\
#     #.show(500, truncate=False)


# thong ke theo status
# query2_df = split_df.groupby('status')\
#             .agg(count('*').alias('count_status'))\
#             .sort(col('count_status').desc())\
#             .show(200, truncate=False)


# thong ke theo http_version
# query3_df = split_df.groupby('http_version')\
#             .agg(count('*').alias('count_http_version'))\
#             .sort(col('count_http_version').desc())\
#             .show(200, truncate=False)


# loc ra http_version khac HTTP/1.1 va HTTP/1.0
# split_df.filter(col('http_version') == '').select(col("value"), col("path")).show(1000, truncate=False)


#thong ke theo method
# query4_df = split_df.groupby('method')\
#             .agg(count('*').alias('count_method'))\
#             .sort(col('count_method').desc())\
#             .show(200, truncate=False)


# loc ra phuong thuoc get ma ko co http version
#split_df.filter((col('http_version') != '') & (col('method') == 'PROPFIND')).select(col("value"), col("path")).show(20, truncate=False)
split_df_filter_http_version = split_df.filter((col('http_version') != '') & (col('http_version') != r"HTTP/1.1\x00"))

# gio thong ke lai theo method
# query5_df = split_df_filter_http_version.groupby('method')\
#             .agg(count('*').alias('count_method'))\
#             .sort(col('count_method').desc())\
#             .show(200, truncate=False)

#loc ra method = 'GET'
split_df_with_get_method = split_df_filter_http_version.filter(col('method')=='GET')

# thong ke lai theo http_version
# query6_df = split_df_with_get_method.groupby('http_version')\
#             .agg(count('*').alias('count_http_version'))\
#             .sort(col('count_http_version').desc())\
#             .show(200, truncate=False)


# in ra utc_ts 
# split_df_with_get_method.select(col('timestamp'), col('utc_ts')).show(200, truncate=False)


# thong kê theo content_size

# query7_df = split_df_with_get_method.groupby('content_size')\
#             .agg(count('*').alias('count_content_size'))\
#             .sort(col('count_content_size').desc())\
#             .show(200, truncate=False)


# # tính avg, min, max của content_size
# query8_df = split_df_with_get_method.select(
#     min('content_size').alias('min_content_size'),
#     max('content_size').alias('max_content_size'),  
#     mean('content_size').alias('mean_content_size'),   
# ).show(100, truncate=False)


# #thong ke theo endpoint
# query9_df = split_df_with_get_method.groupby('endpoint')\
#             .agg(count('*').alias('count_endpoint'))\
#             .sort(col('count_endpoint').desc())\
#             .show(200, truncate=False)


# #thong ke theo endpoint
# query10_df = split_df_with_get_method.groupby('referer')\
#             .agg(count('*').alias('count_referer'))\
#             .sort(col('count_referer').desc())\
#             .show(200, truncate=False)


# #thong ke theo endpoint
# query11_df = split_df_with_get_method.groupby('agent')\
#             .agg(count('*').alias('count_agent'))\
#             .sort(col('count_agent').desc())\
#             .show(200, truncate=False)

# thong ke theo ngay
query12_df = split_df_with_get_method.groupby('utc_dt')\
            .agg(count('*').alias('count_utc_dt'))\
            .sort(col('count_utc_dt').desc())\
            .show(200, truncate=False)
