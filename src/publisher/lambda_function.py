from __future__ import annotations
import json

import os
import logging
from typing import NamedTuple

import boto3


class EnvironParam(NamedTuple):
    LOG_LEVEL: str
    EVENT_SORCE: str
    EVENTBUSNAME: str

    @classmethod
    def of(cls) -> EnvironParam:
        return EnvironParam(**{k: os.environ[k] for k in EnvironParam._fields})


param = EnvironParam.of()
logger = logging.getLogger(__name__)
logger.setLevel(param.LOG_LEVEL)
client = boto3.client("events")


def lambda_handler(event, context):
    logger.info("first lambda start!")
    logger.info(json.dumps(event, indent=2))
    response = client.put_events(
        Entries=[
            {
                "Source": param.EVENT_SORCE,
                "DetailType": "lambda-event",
                "Detail": json.dumps({"message": "first to second"}),
                "EventBusName": param.EVENTBUSNAME,
            }
        ]
    )
    return {
        "status": 200,
        "body": json.dumps(response),
    }
