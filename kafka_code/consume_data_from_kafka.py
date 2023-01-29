import json
from kafka import KafkaConsumer

if __name__=="__main__":
    consumer=KafkaConsumer(
        "demo",
        bootstrap_servers="kafka:9092",
        auto_offset_reset="latest")

    for msg in consumer:
        print(json.loads(msg.value))