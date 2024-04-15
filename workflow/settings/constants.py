import os
from enum import Enum

node_types = {"StartNode": [],
              "EndNode": [],
              "MessageNode": ["status", "message"],
              "ConditionNode": ["condition"]}


class NodeTypes(Enum):
    START = "StartNode"
    MESSAGE = "MessageNode"
    CONDITION = "ConditionNode"
    END = "EndNode"


class YesNo(Enum):
    YES = "yes"
    NO = "no"


POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
IMAGE_FILE_PATH = "C:/Users/petli/PycharmProjects/starnavi_test_task/workflow/graphs/images/img"
