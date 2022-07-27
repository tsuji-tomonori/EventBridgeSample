from __future__ import annotations
import json

import os
import logging
from typing import NamedTuple


class EnvironParam(NamedTuple):
    LOG_LEVEL: str

    @classmethod
    def of(cls) -> EnvironParam:
        return EnvironParam(**{k: os.environ[k] for k in EnvironParam._fields})


param = EnvironParam.of()
logger = logging.getLogger(__name__)
logger.setLevel(param.LOG_LEVEL)


def lambda_handler(event, context):
    logger.info("third lambda start!")
    logger.info(json.dumps(event, indent=2))
    return {
        "status": 200,
    }
