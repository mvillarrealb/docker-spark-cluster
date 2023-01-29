#!bin/bash
~/bin/kafka-topics.sh --create --topic $1 --bootstrap-server kafka:9092

pip3 install kafka-python