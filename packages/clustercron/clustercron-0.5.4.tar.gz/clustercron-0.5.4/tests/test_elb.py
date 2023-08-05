"""
Tests for `clustercron` module.
"""

from __future__ import print_function
from __future__ import unicode_literals

import requests
import responses
from clustercron import elb


class Inst_health_state(object):
    def __init__(self, instance_id, state):
        self.instance_id = instance_id
        self.state = state


def test_Elb_init():
    '''
    Test Elb attributes set by __init__.
    '''
    lb = elb.Elb('mylbname')
    assert lb.__dict__ == {
        'name': 'mylbname',
        'timeout': 3,
    }


@responses.activate
def test_Elb_get_instance_id_gets_instance_id():
    '''
    Test Elb `get_instance_id` gets `instance_id`.
    '''
    URL_INSTANCE_ID = 'http://169.254.169.254/1.0/meta-data/instance-id'
    INSTANCE_ID = 'i-58e224a1'

    responses.add(
        responses.GET,
        URL_INSTANCE_ID,
        status=200,
        content_type='text/plain',
        body=INSTANCE_ID,
    )

    lb = elb.Elb('mylbname')
    instance_id = lb.get_instance_id()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == URL_INSTANCE_ID
    assert responses.calls[0].response.text == INSTANCE_ID
    assert instance_id == INSTANCE_ID


@responses.activate
def test_Elb_get_instance_id_returns_None_on_HTTPError():
    '''
    test Elb get instance id returns None on HTTPError.
    '''
    URL_INSTANCE_ID = 'http://169.254.169.254/1.0/meta-data/instance-id'

    responses.add(
        responses.GET,
        URL_INSTANCE_ID,
        body=requests.exceptions.HTTPError()
    )

    lb = elb.Elb('mylbname')
    instance_id = lb.get_instance_id()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == URL_INSTANCE_ID
    assert instance_id is None


def test_get_inst_health_states_returns_empty_list_at_exception(monkeypatch):
    '''
    Test Elb `clustercron._get_instance_health_states` returns empty list when
    some exception is raised.
    '''
    class ELBConnectionMock(object):
        def get_all_load_balancers(self, load_balancer_names):
            raise Exception('Some exception')

    monkeypatch.setattr('boto.ec2.elb.ELBConnection', ELBConnectionMock)

    lb = elb.Elb('mylbname')
    assert lb._get_instance_health_states() == []


def test_get_inst_health_states_returns_instance_health_states(monkeypatch):
    '''
    Test Elb `clustercron._get_instance_health_states` returns
    intance_health_states
    '''
    instance_health_states = [
        Inst_health_state('i-0fd16fc5011601deb', 'InService'),
        Inst_health_state('i-019c3471ba8e5659a', 'InService'),
    ]

    class LoadBalancerMock(object):
        def get_instance_health(self):
            return instance_health_states

    class ELBConnectionMock(object):
        def get_all_load_balancers(self, load_balancer_names):
            return [LoadBalancerMock()]

    monkeypatch.setattr('boto.ec2.elb.ELBConnection', ELBConnectionMock)

    lb = elb.Elb('mylbname')
    assert lb._get_instance_health_states() == instance_health_states


def test_Elb_master_returns_True(monkeypatch):
    '''
    Test if `Elb.master` returns True
    '''
    instance_health_states = [
        Inst_health_state('i-0fd16fc5011601deb', 'InService'),
        Inst_health_state('i-019c3471ba8e5659a', 'InService'),
    ]
    monkeypatch.setattr(
        elb.Elb,
        'get_instance_id',
        lambda self: 'i-019c3471ba8e5659a',
    )
    monkeypatch.setattr(
        elb.Elb,
        '_get_instance_health_states',
        lambda self: instance_health_states,
    )
    lb = elb.Elb('mylbname')
    assert lb.master() is True


def test_Elb_master_returns_False(monkeypatch):
    '''
    Test if `Elb.master` returns False
    '''
    instance_health_states = [
        Inst_health_state('i-0fd16fc5011601deb', 'InService'),
        Inst_health_state('i-019c3471ba8e5659a', 'InService'),
    ]
    monkeypatch.setattr(
        elb.Elb,
        'get_instance_id',
        lambda self: 'i-0fd16fc5011601deb',
    )
    monkeypatch.setattr(
        elb.Elb,
        '_get_instance_health_states',
        lambda self: instance_health_states,
    )
    lb = elb.Elb('mylbname')
    assert lb.master() is False


def test_Elb_master_returns_False_when_instance_id_is_None(monkeypatch):
    '''
    Test if `Elb.master` returns False when `Elb.instance_id` is None.
    '''
    instance_health_states = [
        Inst_health_state('i-0fd16fc5011601deb', 'InService'),
        Inst_health_state('i-019c3471ba8e5659a', 'InService'),
    ]
    monkeypatch.setattr(
        elb.Elb,
        'get_instance_id',
        lambda self: 'i-0fd16fc5011601deb',
    )
    monkeypatch.setattr(
        elb.Elb,
        '_get_instance_health_states',
        lambda self: instance_health_states,
    )
    lb = elb.Elb('mylbname')
    assert lb.master() is False
