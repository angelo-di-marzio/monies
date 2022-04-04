#!/usr/bin/env python
import pika, requests, sys, os, time, json
from geopy.geocoders import Nominatim

parameters = pika.URLParameters(
    "amqp://rabbitmq:rabbitmqPWD@rabbitmq?connection_attempts=5&retry_delay=5"
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="coordinates", durable=True)

print(" [*] Waiting for messages. To exit press CTRL+C")


def process_coords(ch, method, properties, body):
    user_id = body.decode()
    print(" [x] Received id : %r" % user_id)
    response = requests.get(f"http://api/users/{user_id}")
    user = response.json()
    print(user)
    geolocator = Nominatim(user_agent="Moneys")
    location = geolocator.geocode(user["address"])

    coords = f"{location.latitude}, {location.longitude}"
    print(coords)
    user["coordinates"] = coords
    print(user)
    r = requests.put("http://api/users/", data=json.dumps(user))
    print(r.status_code)
    print(r.json())
    # check if done if not check ack
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="coordinates", on_message_callback=process_coords)

channel.start_consuming()
