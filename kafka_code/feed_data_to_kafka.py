import time,json,random
from datetime import datetime
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode("utf-8")
    
producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=serializer
)

if __name__=="__main__":
    for i in range(10000000):
        dummy_messages= str(i)
        print(f"Producing message {datetime.now()} | Message = {str(dummy_messages)}")
        producer.send("demo",dummy_messages)
        time.sleep(2)