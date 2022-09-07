
from os import environ
from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_ssm as ssm,
    aws_servicediscovery as svc_discovery,
    CfnOutput,
)
from constructs import Construct


class EcsMicroService(Construct):
  def __init__(self, scope: Construct, construct_id: str, name: str,
      uri_base: str,
      directory: str,
      alb: elb.ApplicationLoadBalancer,
      cluster: ecs.Cluster,
      svc_namespace: svc_discovery.INamespace,
      vpc: ec2.Vpc,
      listener: elb.ApplicationListener,
      route_priority: int,
      service_dns_param_name: str = None,
      app_port=8000,
      container_env: dict = None,
      **kwargs
  ):
    super().__init__(scope, construct_id, **kwargs)

    environment = { "PORT": str(app_port) }
    if container_env:
        for k, v in container_env.items():
            environment[k] = v

    task_def = ecs.FargateTaskDefinition(self, "taskdef")
    container = task_def.add_container('app-container',
        environment=environment,
        logging=ecs.LogDriver.aws_logs(stream_prefix="app-container"),
        image=ecs.ContainerImage.from_asset(directory=directory),
        essential=True,
        port_mappings=[ecs.PortMapping(container_port=app_port)],
        health_check=ecs.HealthCheck(command=["CMD-SHELL", f"curl -f http://localhost:{app_port}{uri_base}/health || exit 1"])
    )

    service = ecs.FargateService(self, "fargate-svc", 
        service_name=name,
        cluster=cluster,
        task_definition=task_def,
        desired_count=2,
        cloud_map_options=ecs.CloudMapOptions(
            cloud_map_namespace=svc_namespace,
            name=name
        )
    )

    target_group = elb.ApplicationTargetGroup(self, "target-group", port=app_port, protocol=elb.ApplicationProtocol.HTTP, targets=[service], vpc=vpc)
    elb.ApplicationListenerRule(self, "alb-endpoint-rule",
        listener=listener,
        conditions=[elb.ListenerCondition.path_patterns([f"{uri_base}*"])],
        target_groups=[target_group],
        priority=route_priority)

    if service_dns_param_name:
        ssm.StringParameter(self, "internal-service-dns-param",
            parameter_name=service_dns_param_name,
            string_value=f"{service.cloud_map_service.service_name}.{svc_namespace.namespace_name}")

    CfnOutput(self, "internal-service-dns-name", value=f"{service.cloud_map_service.service_name}.{svc_namespace.namespace_name}")
    CfnOutput(self, "alb-endpoint", value=f"{alb.load_balancer_dns_name}{uri_base}")

    self.task_def = task_def
    self.service = service
    self.target_group = target_group
