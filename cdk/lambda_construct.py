from __future__ import annotations
from typing import NamedTuple

import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
    Duration,
)
from constructs import Construct

from cdk.stack_resource import StackResource


class StandAlonLambdaParam(NamedTuple):
    resource: StackResource
    description_en: str = ""
    description_jp: str = ""
    lambda_code_asset_path: str = "src"
    lambda_handler_path: str = "lambda_function.lambda_handler"
    lambda_runtime: lambda_.Runtime = lambda_.Runtime.PYTHON_3_9
    lambda_environment: dict[str, str] = {"LOG_LEVEL": "INFO"}
    lambda_timeout: Duration.seconds = Duration.seconds(10)
    lambda_memory_size: int = 256
    log_retention: logs.RetentionDays = logs.RetentionDays.THREE_MONTHS
    log_removal_policy: cdk.RemovalPolicy = cdk.RemovalPolicy.RETAIN


class StandAlonLambdaConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, param: StandAlonLambdaParam) -> None:
        super().__init__(scope, construct_id)

        self.role = iam.Role(
            self, param.resource.name("rol"),
            role_name=param.resource.name("rol"),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
            description=param.description_en,
        )

        self.fn = lambda_.Function(
            self, param.resource.name("lmd"),
            code=lambda_.Code.from_asset(param.lambda_code_asset_path),
            handler=param.lambda_handler_path,
            runtime=param.lambda_runtime,
            function_name=param.resource.name("lmd"),
            environment=param.lambda_environment,
            description=param.description_jp,
            timeout=param.lambda_timeout,
            memory_size=param.lambda_memory_size,
            role=self.role,
        )

        self.loggroup = logs.LogGroup(
            self, param.resource.name("logs"),
            log_group_name=f"/aws/lambda/{self.fn.function_name}",
            retention=param.log_retention,
            removal_policy=param.log_removal_policy,
        )
