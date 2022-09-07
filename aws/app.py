#!/usr/bin/env python3
import os
from unicodedata import name

import aws_cdk as cdk

from aws_infra.aws_infra_stack import AwsInfraStack
from add_nums.add_nums_stack import AddNumsStack
from subtract_nums.subtract_nums_stack import SubtractNumsStack
from multiply_nums.multiply_nums_stack import MultiplyNumsStack
from divide_nums.divide_nums_stack import DivideNumsStack
from average_nums.average_nums_stack import AverageNumsStack


app = cdk.App()

env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

infra_stack = AwsInfraStack(app, "calc-infra",
    naming_prefix="calculator-services",
    env=env,
    stack_name="calcuator-infra"
)

add_stack = AddNumsStack(app, "add-num", 
    alb=infra_stack.alb,
    cluster=infra_stack.fargate,
    vpc=infra_stack.vpc,
    listener=infra_stack.alb_listener,
    svc_namespace=infra_stack.svc_namespace,
    route_priority=10,
    env=env,
    stack_name="add-nums"
)

subtract_stack = SubtractNumsStack(app, "subtract-nums",
    alb=infra_stack.alb,
    cluster=infra_stack.fargate,
    vpc=infra_stack.vpc,
    listener=infra_stack.alb_listener,
    svc_namespace=infra_stack.svc_namespace,
    route_priority=20,
    env=env,
    stack_name="subtract-nums"
)

multiply_stack = MultiplyNumsStack(app, "multiply-nums",
    alb=infra_stack.alb,
    cluster=infra_stack.fargate,
    vpc=infra_stack.vpc,
    listener=infra_stack.alb_listener,
    svc_namespace=infra_stack.svc_namespace,
    route_priority=30,
    env=env,
    stack_name="multiply-nums"
)

divide_stack = DivideNumsStack(app, "divide-nums",
    alb=infra_stack.alb,
    cluster=infra_stack.fargate,
    vpc=infra_stack.vpc,
    listener=infra_stack.alb_listener,
    svc_namespace=infra_stack.svc_namespace,
    route_priority=40,
    env=env,
    stack_name="divide-nums"
)

average_stack = AverageNumsStack(app, "average-nums",
    alb=infra_stack.alb,
    cluster=infra_stack.fargate,
    vpc=infra_stack.vpc,
    listener=infra_stack.alb_listener,
    svc_namespace=infra_stack.svc_namespace,
    route_priority=50,
    env=env,
    stack_name="average-nums"
)
average_stack.add_dependency(add_stack)
average_stack.add_dependency(divide_stack)

app.synth()
