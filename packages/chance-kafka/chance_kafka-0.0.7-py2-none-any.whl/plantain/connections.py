#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: plantain/connections.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 26.04.2018
from functools import wraps
from confluent_kafka import Producer as KafkaProducer

from plantain.consumer import Consumer
import logging


LOGGER = logging.getLogger()


class WrapProducer(object):
    """Wrap class for producer
    """
    def __init__(self, config):
        self._producer = KafkaProducer(config, logger=LOGGER)

    def send(self, topic, message):
        self._producer.poll(1.0)
        self._producer.produce(topic, message)

    def flush(self):
        self._producer.flush()


class KafkaConnection(object):
    """Class for kafka connection
    """
    bootstrap_servers = None
    producer = None

    @classmethod
    def connect(cls, bootstrap_servers):
        """Get server configs and create producer

        Args:
            bootstrap_servers: ([str]) a list of server addr
            default_producer: (bool) whether producer is created.
        """
        cls.bootstrap_servers = bootstrap_servers
        cls.config = {'bootstrap.servers': cls.bootstrap_servers}

        cls.producer = WrapProducer(cls.config)

    @classmethod
    def close(cls):
        """Close producer
        """
        cls.producer.flush()
        cls.producer = None

    @classmethod
    def with_producer(cls):
        """Decorator for introducing producer

        Wrap the function with the static producer.

        Example:

        .. code-block:: python

            @with_producer
            def A(some_arguments, producer):
                pass

        Notice that only in keywords can you pass your own producer rather than
        the given, or a TypeError will raise for multiple arguments
        of producer passed into the same function. In other works, following
        code will raise a TypeError:

        .. code-block:: python

            @with_producer
            def A(some_arguments, producer):
                pass

            A('test', your_own_producer) # Raise TypeError
            A('test', producer=your_own_producer) # Safe

        Return:
            a wrapped func
        """
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                producer = kwargs.pop('producer', cls.producer)
                kwargs['producer'] = producer

                return func(*args, **kwargs)

            return wrapper
        return decorator

    @classmethod
    def create_consumer(
        cls, topics, timeout, offset, group_id, max_poll_interval_ms=600000,
        max_poll_records=100
    ):
        """Create consumer with given args

        Args:
            topic: (str / [str]) a list of str or a str as listened topics
            timeout: (int or None) the timeout before close consumer, or not
            close when is set to None.
            offset: (str) the offset in the topic, 'latest' or 'earlist'.
            group_id: (str) the group of consumer
            max_poll_interval_ms: (int) max delay between poll. Default 600000
            max_poll_records: (int) max records returned in a poll. Default 100

        Return:
            (consumer.Consumer)
        """
        if isinstance(topics, basestring):
            topics = [topics]

        return Consumer(
            cls.bootstrap_servers, *topics, timeout_ms=timeout, offset=offset,
            group_id=group_id,
            max_poll_interval_ms=max_poll_interval_ms,
            max_poll_records=max_poll_records
        )
