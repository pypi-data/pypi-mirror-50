# -*- coding:utf-8 -*-
# pylint: disable=W0703

""" kafka_utils 

"""


from kdkafka import kafka_api


KAFKA_PRODUCERS = {}


def _get_kafka_producer(hosts, topic):
    if topic not in KAFKA_PRODUCERS:
        KAFKA_PRODUCERS[topic] = kafka_api.get_producer(hosts, topic) 
    return KAFKA_PRODUCERS[topic]


def kafka_produce(hosts, topic, value):
    producer = _get_kafka_producer(hosts, topic)
    kafka_api.produce(producer, value)
    return True

    

