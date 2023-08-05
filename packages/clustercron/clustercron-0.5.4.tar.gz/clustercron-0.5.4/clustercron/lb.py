# clustercron/lb.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.lb
---------------

Modules holds base class for AWS ElasticLoadBalancing classes
'''

from __future__ import unicode_literals

import logging
import requests


logger = logging.getLogger(__name__)


class Lb(object):
    URL_INSTANCE_ID = \
        'http://169.254.169.254/1.0/meta-data/instance-id'

    def __init__(self, name, timeout=3):
        '''
        :param name: name of load balancer or target group
        :param timeout: timeout in seconds
        '''
        self.name = name
        self.timeout = timeout

    def get_instance_id(self):
        instance_id = None
        logger.debug('Get instance ID')
        try:
            response = requests.get(self.URL_INSTANCE_ID, timeout=self.timeout)
        except Exception as error:
            logger.error('Could not get Instance ID: %s', error)
        else:
            instance_id = response.text
            logger.info('Instance ID: %s', instance_id)
        return instance_id

    def get_healty_instances(self):
        raise NotImplementedError

    def master(self):
        logger.debug('Check if instance is master')
        instance_id = self.get_instance_id()
        if instance_id:
            healty_instances = self.get_healty_instances()
            if healty_instances:
                return instance_id == healty_instances[0]
        return False
