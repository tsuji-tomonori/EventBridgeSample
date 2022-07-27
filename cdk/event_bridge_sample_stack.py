from __future__ import annotations

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Tags,
)
from constructs import Construct

from cdk.stack_resource import StackResource, DeployEnv
from cdk.event_construct import EventRuleParam, EventRuleConstruct
from cdk.lambda_construct import StandAlonLambdaParam, StandAlonLambdaConstruct


class EventBridgeSampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pub_constructs = {}
        for message_type in ("publisher", "forward"):
            pub_param = StandAlonLambdaParam(
                resource=StackResource(
                    deploy_env=DeployEnv.DEV,
                    construct_name=f"EventBridgeSample{message_type.capitalize()}"
                ),
                lambda_code_asset_path=f"src/{message_type}",
                lambda_environment=self.node.try_get_context(
                    f"{message_type}_env"
                ),
                log_removal_policy=cdk.RemovalPolicy.DESTROY,
            )
            pub_construct = StandAlonLambdaConstruct(
                self, f"{message_type}_construct",
                param=pub_param
            )
            pub_constructs[message_type] = pub_construct
            Tags.of(pub_construct).add("Construct", message_type)

        sub_fns = []
        for i in range(self.node.try_get_context("subscriber_num")):
            sub_param = StandAlonLambdaParam(
                resource=StackResource(
                    deploy_env=DeployEnv.DEV,
                    construct_name=f"EventBridgeSampleSubscriber{i}"
                ),
                lambda_code_asset_path="src/subscriber",
                lambda_environment=self.node.try_get_context(
                    "subscriber_env"
                ),
                log_removal_policy=cdk.RemovalPolicy.DESTROY,
            )
            sub_construct = StandAlonLambdaConstruct(
                self, f"subscriber_construct_{i}",
                param=sub_param
            )
            sub_fns.append(sub_construct.fn)
            Tags.of(sub_construct).add("Construct", "subscriber")

        event_param = EventRuleParam(
            resource=StackResource(
                deploy_env=DeployEnv.DEV,
                construct_name="EventBridgeSample"
            ),
            from_first=[pub_constructs["forward"].fn],
            from_second=sub_fns,
        )
        event_construct = EventRuleConstruct(
            self, "event_construct",
            param=event_param,
        )
        Tags.of(event_construct).add("Construct", "event")

        for con in pub_constructs.values():
            event_construct.event_bus.grant_put_events_to(con.role)
            con.fn.add_environment(
                key="EVENTBUSNAME",
                value=event_construct.event_bus.event_bus_name,
            )
