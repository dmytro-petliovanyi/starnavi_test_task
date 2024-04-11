from typing import Optional

from pydantic import BaseModel, field_validator

from workflow.db.models import Node


class NodeBase(BaseModel):
    name: str
    node_type: str
    status: Optional[str] = None
    message: Optional[str] = None


class NodeSchema(NodeBase):
    id: int

    class Config:
        orm_mode = True


class EdgeBase(BaseModel):
    node_id: int
    next_node_id: int


class EdgeSchema(EdgeBase):
    id: int

    class Config:
        orm_mode = True


class WorkflowBase(BaseModel):
    name: str
    status: Optional[str] = None


class WorkflowSchema(WorkflowBase):
    id: int
    nodes: list[Node] = []

    class Config:
        orm_mode = True


class RequestNodeSchema(BaseModel):
    name: str
    node_type: str
    status: str
    message: str

    @field_validator('name')
    def validate_name(cls, name: str):
        name = name.strip()
        if not name:
            raise ValueError("name cannot be empty")
        return name

    @field_validator('node_type')
    def validate_node_type(cls, node_type: str):
        node_type = node_type.strip()
        if not node_type:
            raise ValueError("node_type cannot be empty")
        return node_type

    @field_validator('status')
    def validate_status(cls, status: str):
        status = status.strip()
        if not status:
            raise ValueError("status cannot be empty")
        return status

    @field_validator('message')
    def validate_message(cls, message: str):
        message = message.strip()
        if not message:
            raise ValueError("message cannot be empty")
        return message


class RequestEdgeSchema(BaseModel):
    node_id: int
    next_node_id: int

    @field_validator("node_id")
    def validate_node_id(cls, node_id: int):
        if node_id <= 0:
            raise ValueError("Node ID must be a positive integer")

        return node_id

    @field_validator("next_node_id")
    def validate_next_node_id(cls, next_node_id: int):
        if next_node_id <= 0:
            raise ValueError("Next Node ID must be a positive integer")

        return next_node_id


class RequestWorkflowSchema(BaseModel):
    name: str
    status: str

    @field_validator("name")
    def validate_name(cls, name: str):
        name = name.strip()
        if not name.isalnum():
            raise ValueError("Invalid name, should contain only alphanumeric characters")
        return name

    @field_validator("status")
    def validate_status(cls, status: str):
        status = status.strip()
        if not status.isalnum():
            raise ValueError("Invalid status, should contain only alphanumeric characters")
        return status
