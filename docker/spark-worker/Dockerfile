FROM spark-base:latest

COPY start-worker.sh /

ENV SPARK_WORKER_WEBUI_PORT=8081
ENV SPARK_WORKER_LOG=${SPARK_HOME}/logs
ENV SPARK_MASTER="spark://spark-master:7077"

EXPOSE 8081

CMD ["/bin/bash", "/start-worker.sh"]
