from __future__ import annotations

import aws_cdk
from aws_cdk import Tags

from cdk.event_bridge_sample_stack import EventBridgeSampleStack

app = aws_cdk.App()
stack = EventBridgeSampleStack(
    app,
    "EventBridgeSampleStack",
    stack_name="EventBridgeSampleStack",
    description="Test Event driven architecture"
)

Tags.of(stack).add("Project", "EventBridgeSample")
Tags.of(stack).add("Type", "Test")

app.synth()
