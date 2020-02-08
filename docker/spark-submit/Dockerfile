FROM spark-base:latest

COPY spark-submit.sh /

ENV SPARK_MASTER_URL="spark://spark-master:7077"
ENV SPARK_SUBMIT_ARGS=""
ENV SPARK_APPLICATION_ARGS ""
#ENV SPARK_APPLICATION_JAR_LOCATION /opt/spark-apps/myjar.jar
#ENV SPARK_APPLICATION_MAIN_CLASS my.main.Application


CMD ["/bin/bash", "/spark-submit.sh"]
