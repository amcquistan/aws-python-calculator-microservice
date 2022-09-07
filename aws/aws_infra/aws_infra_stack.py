from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elb,
    aws_servicediscovery as service_disc,
    aws_ssm as ssm,
    Stack,
    CfnOutput
)
from constructs import Construct

class AwsInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, naming_prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "vpc", max_azs=2)
        vpc_param = ssm.StringParameter(self, "vpc-ssm-param",
                string_value=vpc.vpc_id,
                parameter_name=f"/{naming_prefix}/vpc-id"
        )

        fargate = ecs.Cluster(self, "fargate-cluster", vpc=vpc)
        fargate_param = ssm.StringParameter(self, "fargate-ssm-param",
                string_value=fargate.cluster_arn,
                parameter_name=f"/{naming_prefix}/fargate-arn"
        )

        alb_security_group = ec2.SecurityGroup(self, "lb-seg", vpc=vpc)
        alb_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.all_icmp())
        alb_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.all_tcp())
        alb_security_group.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.all_traffic())

        alb = elb.ApplicationLoadBalancer(self, "loadbalancer", 
                vpc=vpc,
                internet_facing=True,
                security_group=alb_security_group
        )
        
        alb_ssm = ssm.StringParameter(self, "alb-ssm-param", string_value=alb.load_balancer_arn, parameter_name=f"/{naming_prefix}/alb-arn")

        listener = alb.add_listener("listener",
                port=80,
                protocol=elb.ApplicationProtocol.HTTP,
                open=True,
                default_action=elb.ListenerAction.fixed_response(status_code=404, content_type="application/json",
                message_body='{"message": "Resource not found."}'))
        alb_listener_ssm = ssm.StringParameter(self, "alb-listener-ssm-param", string_value=listener.listener_arn, parameter_name=f"/{naming_prefix}/alb-listener-arn")

        svc_namespace = service_disc.PrivateDnsNamespace(self, "private-dns-svc-reg",
                vpc=vpc,
                name="calculator.local"
        )

        CfnOutput(self, "vpc-id", value=vpc.vpc_id)
        CfnOutput(self, "vpc-id-param", value=vpc_param.parameter_name)
        CfnOutput(self, "fargate-arn", value=fargate.cluster_arn)
        CfnOutput(self, "fargate-arn-param", value=fargate_param.parameter_name)
        CfnOutput(self, "alb-arn", value=alb.load_balancer_arn)
        CfnOutput(self, "alb-arn-param", value=alb_ssm.parameter_name)
        CfnOutput(self, "alb-listener-arn", value=listener.listener_arn)
        CfnOutput(self, "alb-listener-arn-param", value=alb_listener_ssm.parameter_name)
        CfnOutput(self, "private-dns-svc-reg-arn", value=svc_namespace.namespace_arn)

        self.vpc = vpc
        self.fargate = fargate
        self.alb_security_group = alb_security_group
        self.alb = alb
        self.alb_listener = listener
        self.svc_namespace = svc_namespace
