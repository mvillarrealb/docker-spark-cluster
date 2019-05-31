source ./.env

LOCAL_JAR_FOLDER="/data/poteng/workspace/spark-learn/spark/target"
JAR_NAME="spark-examples-1.0-SNAPSHOT.jar"
MAIN_CLASS="spark.Pi"

# copy files to host folder defined in .env
mkdir -p ${HOST_APP_FOLDER}
mkdir -p ${HOST_DATA_FOLDER}
cp ${LOCAL_JAR_FOLDER}/${JAR_NAME} ${HOST_APP_FOLDER}

SPARK_APPLICATION_JAR_LOCATION="/opt/spark-apps/$JAR_NAME"

docker run --network docker-spark-cluster_spark-network \
-v ${HOST_APP_FOLDER}:/opt/spark-apps \
--env SPARK_APPLICATION_JAR_LOCATION=$SPARK_APPLICATION_JAR_LOCATION \
--env SPARK_APPLICATION_MAIN_CLASS=$MAIN_CLASS \
spark-submit:${SPARK_VERSION} sh spark-submit.sh

