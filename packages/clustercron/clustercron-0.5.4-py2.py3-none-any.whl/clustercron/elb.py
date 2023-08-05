# clustercron/elb.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.elb
---------------

Modules holds class for AWS ElasticLoadBalancing (ELB)
'''

from __future__ import unicode_literals

import logging
import boto.ec2.elb

from .lb import Lb


logger = logging.getLogger(__name__)


class Elb(Lb):
    def _get_instance_health_states(self):
        inst_health_states = []
        logger.debug('Get instance health states')
        try:
            conn = boto.ec2.elb.ELBConnection()
            lb = conn.get_all_load_balancers(
                load_balancer_names=[self.name])[0]
            inst_health_states = lb.get_instance_health()
        except Exception as error:
            logger.error('Could not get instance health states: %s', error)
        return inst_health_states

    def get_healty_instances(self):
        healty_instances = []
        inst_health_states = self._get_instance_health_states()
        if inst_health_states:
            logger.debug('Instance health states: %s', inst_health_states)
            try:
                healty_instances = sorted(
                    x.instance_id for x in inst_health_states
                    if x.state == 'InService'
                )
            except Exception as error:
                logger.error('Could not parse healty_instances: %s', error)
            else:
                logger.info(
                    'Healty instances: %s', ', '.join(healty_instances)
                )
        return healty_instances
