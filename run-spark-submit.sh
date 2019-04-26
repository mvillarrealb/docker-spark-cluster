source ./.env

LOCAL_JAR_FOLDER="/data/poteng/workspace/spark-learn/spark/target"
JAR_NAME="spark-examples-1.0-SNAPSHOT.jar"
MAIN_CLASS="mygroup.spark.Pi"

# copy files to host folder
mkdir -p ${HOST_APP_FOLDER}
mkdir -p ${HOST_DATA_FOLDER}
cp ${LOCAL_JAR_FOLDER}/${JAR_NAME} ${HOST_APP_FOLDER}

SPARK_APPLICATION_JAR_LOCATION="/opt/spark-apps/$JAR_NAME"
SPARK_SUBMIT_ARGS="--conf spark.executor.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf'"

docker run --network docker-spark-cluster_spark-network \
-v ${HOST_APP_FOLDER}:/opt/spark-apps \
--env SPARK_APPLICATION_JAR_LOCATION=$SPARK_APPLICATION_JAR_LOCATION \
--env SPARK_APPLICATION_MAIN_CLASS=$MAIN_CLASS \
spark-submit:${SPARK_VERSION}

