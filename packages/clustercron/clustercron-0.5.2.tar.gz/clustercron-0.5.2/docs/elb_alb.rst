.. _clustercron-elb-alb:

Clustercron AWS LB
==================

Clustercron ELB
---------------

Clustercron in ELB mode will retrieve the instance ID of the instance (node in
a load balanced cluster) it is running on. After retrieving the *health states*
of all the nodes in the *load balancer group*, clustercron checks if the node's
instance ID is the first in the (alphabetic) list of instances that have the
state *InService*. If so it will consider the node *master* and will run the
given *command*. If no command is given clustercron will exit 0 if the node is
considered *master* else clustercron will return 1.


Clustercron ALB
---------------

Clustercron in ALB mode will retrieve the instance ID of the instance (node in
a target group) it is running in. After retrieving the *health states* of all
the nodes in the *target group*, clustercron checks if the node's instance ID
is the first in the (alphabetic) list of instances that have the state
*healthy*.  If so it will consider the node *master* and will run the given
*command*. If no command is given clustercron will exit 0 if the node is
considered *master* else clustercron will return 1.


Cron job times and clustercron timeouts
---------------------------------------

Cron jobs wrapped with *Clustercron* should be started on the same time on
every node in the cluster. For syncronized time a NTP (or Chrony) client is
strongly advised.

Clusteron's timeout and retries settings should be minimized to syncronize
clustercron runs as much as possible. A time out of 2 seconds and a maximum of
1 retry is advised.

These options must be set in the `Boto Config`_.


Boto config and credentials (ELB)
---------------------------------

*Clustercron ELB* uses boto_, A Python interface to Amazon Web Services.
*Clustercron ELB* depends on boto_'s configuration and access management.

A boto configuration file, placed in the users home directory, `~/.boto`, can
be used for both configuration and credentials.  Alternatively a AWS credential
file, `~/.aws/credentials`, can be used for credentials shared between
different AWS SDKs.

See `Boto Config`_ documention for further details.

Make sure the following `Boto Config`_ options are set:

    * elb_region_name

    * elb_region_endpoint

    * http_socket_timeout = 2

    * num_retries = 1


Example configuration `~/.boto`::

    [Credentials]
    aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
    aws_secret_access_key = lMSnv8MeCOxUphBX6LRHK7e6QkLwKiEVgvKKOqVG

    [Boto]
    elb_region_name = eu-west-1
    elb_region_endpoint = elasticloadbalancing.eu-west-1.amazonaws.com
    http_socket_timeout = 2
    num_retries = 1


The user for checking the AWS load balancers has to have the following read rights.

example AWS policy::

  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "elasticloadbalancing:DescribeInstanceHealth",
                  "elasticloadbalancing:DescribeLoadBalancerAttributes",
                  "elasticloadbalancing:DescribeLoadBalancerPolicyTypes",
                  "elasticloadbalancing:DescribeLoadBalancerPolicies",
                  "elasticloadbalancing:DescribeLoadBalancers",
                  "elasticloadbalancing:DescribeTags"
              ],
              "Resource": "*"
          }
      ]
  }


AWS config and credentials (ALB)
---------------------------------

*Clustercron ALB* uses boto3_, which is a new version of the boto library based
on botocore_. *Clustercron ALB* just can do with AWS credential file,
`~/.aws/credentials`, and AWS configuration file, `~/.aws/config`.
*Clustercron ALB* needs a **AWS region** to be set as a minimal configuration 

Example configuration `~/.aws/config`::

  [default]
  region = eu-west-1


The user (or role) for checking the AWS **Target Groups** has to have the
following read rights.

example AWS policy::

  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "elasticloadbalancing:DescribeTargetGroups",
                  "elasticloadbalancing:DescribeTargetHealth"
              ],
              "Resource": "*"
          }
      ]
  }


.. _boto: http://boto.cloudhackers.com/en/latest/
.. _boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
.. _botocore: https://github.com/boto/botocore
.. _Boto Config: http://boto.readthedocs.org/en/latest/boto_config_tut.html
