#!/usr/bin/env python
import pika
import sys


def add_to_queue(data):
    credentials = pika.PlainCredentials("rabbitmq", "rabbitmqPWD")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="coordinates", durable=True)
    channel.basic_publish(
        exchange="",  # default exchange
        routing_key="coordinates",
        body=str(data),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    print(" [x] Sent %r" % data)
    connection.close()
