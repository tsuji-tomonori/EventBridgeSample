from __future__ import annotations

from typing import NamedTuple

from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as target,
)
from constructs import Construct

from cdk.stack_resource import StackResource


class EventRuleParam(NamedTuple):
    resource: StackResource
    from_first: list[lambda_.Function]
    from_second: list[lambda_.Function]


class EventRuleConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, param: EventRuleParam) -> None:
        super().__init__(scope, construct_id)

        self.event_bus = events.EventBus(
            self, param.resource.name("bus"),
            event_bus_name=param.resource.name("bus")
        )

        self.first = events.Rule(
            self, param.resource.name("rul_first"),
            rule_name=param.resource.name("rul_first"),
            event_bus=self.event_bus,
            event_pattern=events.EventPattern(
                source=["custom.event.first"],
            ),
            targets=[target.LambdaFunction(fn) for fn in param.from_first],
        )

        self.second = events.Rule(
            self, param.resource.name("rul_second"),
            rule_name=param.resource.name("rul_second"),
            event_bus=self.event_bus,
            event_pattern=events.EventPattern(
                source=["custom.event.second"],
            ),
            targets=[target.LambdaFunction(fn) for fn in param.from_second],
        )
