#!/bin/bash

set -e

docker build -t spark-base:latest ./docker/base
docker build -t spark-master:latest ./docker/spark-master
docker build -t spark-worker:latest ./docker/spark-worker
docker build -t spark-submit:latest ./docker/spark-submit