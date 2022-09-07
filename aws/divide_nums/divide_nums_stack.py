from pathlib import Path

from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_servicediscovery as svc_discovery,
    Stack,
)
from constructs import Construct


from common import EcsMicroService, constants as c


class DivideNumsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, alb: elb.ApplicationLoadBalancer, cluster: ecs.Cluster, vpc: ec2.Vpc, listener: elb.ApplicationListener, svc_namespace: svc_discovery.INamespace, route_priority: int, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        EcsMicroService(self, "divide-svc",
            name="divide",
            uri_base="/divide",
            directory=str(Path(__file__).resolve().parents[2].joinpath("divide_nums")),
            alb=alb,
            cluster=cluster,
            svc_namespace=svc_namespace,
            vpc=vpc,
            listener=listener,
            route_priority=route_priority,
            service_dns_param_name=c.AWS_SSM_DIVIDE_ENDPOINT
        )
