# Spark Cluster with Docker & docker-compose(2021 ver.)

# General

A simple spark standalone cluster for your testing environment purposses. A *docker-compose up* away from you solution for your spark development environment.

The Docker compose will create the following containers:

container|Exposed ports
---|---
spark-master|9090 7077
spark-worker-1|9091
spark-worker-2|9092
demo-database|5432

# Installation

The following steps will make you run your spark cluster's containers.

## Pre requisites

* Docker installed

* Docker compose  installed

## Build the image


```sh
docker build -t cluster-apache-spark:3.0.2 .
```

## Run the docker-compose

The final step to create your test cluster will be to run the compose file:

```sh
docker-compose up -d
```

## Validate your cluster

Just validate your cluster accesing the spark UI on each worker & master URL.

### Spark Master

http://localhost:9090/

![alt text](docs/spark-master.png "Spark master UI")

### Spark Worker 1

http://localhost:9091/

![alt text](docs/spark-worker-1.png "Spark worker 1 UI")

### Spark Worker 2

http://localhost:9092/

![alt text](docs/spark-worker-2.png "Spark worker 2 UI")


# Resource Allocation 

This cluster is shipped with three workers and one spark master, each of these has a particular set of resource allocation(basically RAM & cpu cores allocation).

* The default CPU cores allocation for each spark worker is 1 core.

* The default RAM for each spark-worker is 1024 MB.

* The default RAM allocation for spark executors is 256mb.

* The default RAM allocation for spark driver is 128mb

* If you wish to modify this allocations just edit the env/spark-worker.sh file.

# Binded Volumes

To make app running easier I've shipped two volume mounts described in the following chart:

Host Mount|Container Mount|Purposse
---|---|---
apps|/opt/spark-apps|Used to make available your app's jars on all workers & master
data|/opt/spark-data| Used to make available your app's data on all workers & master

This is basically a dummy DFS created from docker Volumes...(maybe not...)

# Run a sample application

Now let`s make a **wild spark submit** to validate the distributed nature of our new toy following these steps:

## Run the example




## Run the example with the spark-submit 

```bash
#Creating some variables to make the docker run command more readable
#App jar environment used by the spark-submit image
SPARK_APPLICATION_JAR_LOCATION="/opt/spark-apps/crimes-app.jar"
#App main class environment used by the spark-submit image
SPARK_APPLICATION_MAIN_CLASS="org.mvb.applications.CrimesApp"
#Extra submit args used by the spark-submit image
SPARK_SUBMIT_ARGS="--conf spark.executor.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf'"

#We have to use the same network as the spark cluster(internally the image resolves spark master as spark://spark-master:7077)
docker run --network docker-spark-cluster_spark-network \
-v /mnt/spark-apps:/opt/spark-apps \
--env SPARK_APPLICATION_JAR_LOCATION=$SPARK_APPLICATION_JAR_LOCATION \
--env SPARK_APPLICATION_MAIN_CLASS=$SPARK_APPLICATION_MAIN_CLASS \
spark-submit:2.3.1

```

After running this you will see an output pretty much like this:

```bash
Running Spark using the REST application submission protocol.
2018-09-23 15:17:52 INFO  RestSubmissionClient:54 - Submitting a request to launch an application in spark://spark-master:6066.
2018-09-23 15:17:53 INFO  RestSubmissionClient:54 - Submission successfully created as driver-20180923151753-0000. Polling submission state...
2018-09-23 15:17:53 INFO  RestSubmissionClient:54 - Submitting a request for the status of submission driver-20180923151753-0000 in spark://spark-master:6066.
2018-09-23 15:17:53 INFO  RestSubmissionClient:54 - State of driver driver-20180923151753-0000 is now RUNNING.
2018-09-23 15:17:53 INFO  RestSubmissionClient:54 - Driver is running on worker worker-20180923151711-10.5.0.4-45381 at 10.5.0.4:45381.
2018-09-23 15:17:53 INFO  RestSubmissionClient:54 - Server responded with CreateSubmissionResponse:
{
  "action" : "CreateSubmissionResponse",
  "message" : "Driver successfully submitted as driver-20180923151753-0000",
  "serverSparkVersion" : "2.3.1",
  "submissionId" : "driver-20180923151753-0000",
  "success" : true
}
```

# Summary (What have I done :O?)

* We compiled the necessary docker images to run spark master and worker containers.

* We created a spark standalone cluster using 3 worker nodes and 1 master node using docker && docker-compose.

* Copied the resources necessary to run a sample application.

* Submitted an application to the cluster using a **spark-submit** docker image.

* We ran a distributed application at home(just need enough cpu cores and RAM to do so).

# Why a standalone cluster?

* This is intended to be used for test purposes, basically a way of running distributed spark apps on your laptop or desktop.

* Right now I don't have enough resources to make a Yarn, Mesos or Kubernetes based cluster :(.

* This will be useful to use CI/CD pipelines for your spark apps(A really difficult and hot topic)

# Steps to connect and use a pyspark shell interactively

* Follow the steps to run the docker-compose file. You can scale this down if needed to 1 worker. 

```bash
docker-compose up --scale spark-worker=1
docker exec -it docker-spark-cluster_spark-worker_1 bash
apt update
apt install python3-pip
pip3 install pyspark
pyspark
```

/opt/spark/bin/spark-submit --jars /opt/spark-apps/postgresql-42.2.22.jar --master spark://spark-master:7077 --total-executor-cores 1 /opt/spark-apps/main.py


#!/bin/bash
SPARK_APPLICATION_JAR_LOCATION="/opt/spark-apps/crimes-app.jar"
SPARK_APPLICATION_MAIN_CLASS="org.mvb.applications.CrimesApp"
SPARK_SUBMIT_ARGS="--conf spark.executor.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf'"

docker run --network docker-spark-cluster_spark-network -v /mnt/spark-apps:/opt/spark-apps --env SPARK_APPLICATION_JAR_LOCATION=$SPARK_APPLICATION_JAR_LOCATION --env SPARK_APPLICATION_MAIN_CLASS=$SPARK_APPLICATION_MAIN_CLASS spark-submit:2.3.1


./spark-submit --class org.mvb.applications.CrimesApp --master spark://spark-master:6066 --driver-memory 256m --deploy-mode cluster --conf spark.executor.memory='256m' --conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf' /opt/spark-apps/crimes-app.jar


./spark-submit --class org.mvb.applications.CrimesApp --master spark://spark-master:6066 --deploy-mode cluster --conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf' /opt/spark-apps/crimes-app.jar


./spark-submit --class org.mvb.applications.CrimesApp --master spark://spark-master:7077 --conf spark.executor.memory='256m' --conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/dev/config.conf' /opt/spark-apps/crimes-app.jar
 

 docker build -t cluster-apache-spark:3.0.2 .




/opt/spark/bin/spark-submit --class mta.processing.MTAStatisticsApp --master spark://spark-master:7077 --deploy-mode cluster --jars /opt/spark-apps/postgresql-42.2.22.jar --conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/mta.conf' /opt/spark-apps/mta-processing.jar