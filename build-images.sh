#!/bin/bash

set -e

docker build -t spark-base:2.3.1 ./docker/base
docker build -t spark-master:2.3.1 ./docker/spark-master
docker build -t spark-worker:2.3.1 ./docker/spark-worker
docker build -t spark-submit:2.3.1 ./docker/spark-submit