#!/bin/bash

set -e

source ./.env

docker build -t spark-base:${SPARK_VERSION} ./docker/base --build-arg SPARK_VERSION=${SPARK_VERSION}
docker build -t spark-master:${SPARK_VERSION} ./docker/spark-master --build-arg FROM_IMAGE=spark-base:${SPARK_VERSION}
docker build -t spark-worker:${SPARK_VERSION} ./docker/spark-worker --build-arg FROM_IMAGE=spark-base:${SPARK_VERSION}
docker build -t spark-submit:${SPARK_VERSION} ./docker/spark-submit --build-arg FROM_IMAGE=spark-base:${SPARK_VERSION}
