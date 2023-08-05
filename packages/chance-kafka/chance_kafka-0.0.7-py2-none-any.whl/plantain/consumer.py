#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: plantain/consumer.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 26.04.2018
import json
import logging

from confluent_kafka import Consumer as KafkaConsumer


LOGGER = logging.getLogger(__name__)


class WrapMessage(object):
    """Wrapper for kafka message
    """
    def __init__(self, msg):
        self.msg = msg
        self.empty = msg is None or msg.error()
        self.error = self.empty or "Receive nothing from broker in given ms"
        self.value = None if self.empty else self.msg.value()
        self.timestamp = None if self.empty else self.msg.timestamp()[-1]


class WrapConsumer(object):
    """Wrapper for kafka consumer
    """
    def __init__(self, config, topics, timeout):
        self._consumer = KafkaConsumer(config, logger=LOGGER)
        self.topics = list(topics)
        try:
            self.timeout = timeout / 1000.0
        except (TypeError, ValueError):
            self.timeout = -1
        self._consumer.subscribe(self.topics)

    def __iter__(self):
        return self

    def next(self):
        msg = WrapMessage(self._consumer.poll(timeout=self.timeout))
        if msg.empty:
            raise StopIteration()
        return msg

    def close(self):
        self._consumer.close()


class Consumer(object):
    """Class for managing consumer context
    """
    def __init__(self, bootstrap_servers, *topics, **args):
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.timeout = args['timeout_ms']
        self.offset = args['offset']
        self.group_id = args['group_id']
        self.max_poll_interval_ms = args['max_poll_interval_ms']
        self.max_poll_records = args['max_poll_records']
        self.config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': self.offset,
            'session.timeout.ms': 30000,
        }

    def __enter__(self):
        LOGGER.info('Start consumer with {}'.format(self))

        self.consumer = WrapConsumer(self.config, self.topics, self.timeout)
        return self.consumer

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.consumer.close()
        if exc_tb is not None:
            LOGGER.info('Exit consumer with {0}: {1}'.format(
                exc_type, exc_value)
            )
            raise exc_value
        else:
            LOGGER.info('Exit consumer normal')

    def __str__(self):
        value_dict = dict(self.config)
        del value_dict['bootstrap.servers']
        return json.dumps(value_dict)
