from kafka import KafkaProducer
import json


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
with open('inputfile.txt') as f:
    lines = f.readlines()

for line in lines:
    print("Printing", line)
    producer.send('quickstart-events', json.dumps({"Content": line}).encode('utf-8'))
