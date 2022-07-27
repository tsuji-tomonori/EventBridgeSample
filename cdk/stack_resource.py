from __future__ import annotations
import enum
from typing import NamedTuple


class DeployEnv(enum.Enum):
    DEV = "dev"
    PRE = "pre"
    PRO = "pro"


class StackResource(NamedTuple):
    deploy_env: DeployEnv
    construct_name: str

    def name(self, aws_resource_name: str) -> str:
        return f"{self.deploy_env.value}_{aws_resource_name}_{self.construct_name}_cdk"
