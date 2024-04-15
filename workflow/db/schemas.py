from typing import Optional

from pydantic import BaseModel, field_validator

from workflow.settings.constants import NodeTypes


class NodeBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class NodeSchema(NodeBase):
    name: str
    node_type: str
    status: Optional[str] = None
    message: Optional[str] = None
    condition: Optional[str] = None


class EdgeBase(BaseModel):
    node_id: int
    next_node_id: int
    yes_or_no: str


class EdgeSchema(EdgeBase):
    id: int

    class Config:
        orm_mode = True


class WorkflowBase(BaseModel):
    name: str
    status: Optional[str] = None


class WorkflowSchema(WorkflowBase):
    id: int
    nodes: list[NodeBase] = []

    class Config:
        orm_mode = True


class DefaultResponseModel(BaseModel):
    message: str


class RequestNodeSchema(BaseModel):
    name: str
    node_type: str
    status: str
    message: str
    condition: str

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

    @field_validator('status', 'node_type')
    def validate_status(cls, status: str, node_type: str):
        status = status.strip()
        if not status and node_type != NodeTypes.MESSAGE.value:
            raise ValueError("status cannot be empty")
        return status

    @field_validator('message', 'node_type')
    def validate_message(cls, message: str, node_type: str):
        message = message.strip()
        if not message and node_type != NodeTypes.MESSAGE.value:
            raise ValueError("message cannot be empty")
        return message

    @field_validator('condition', 'node_type')
    def validate_condition(cls, condition: str, node_type: str):
        message = condition.strip()
        if not condition and node_type != NodeTypes.CONDITION.value:
            raise ValueError("message cannot be empty")
        return message


class RequestEdgeSchema(BaseModel):
    node_id: int
    next_node_id: int
    yes_or_no: Optional[str] = None

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

    @field_validator("yes_or_no")
    def validate_yes_or_no(cls, yes_or_no: str, values):
        if yes_or_no is not None:
            yes_or_no = yes_or_no.capitalize()

            if yes_or_no not in {"Yes", "No"}:
                raise ValueError('yes_or_no must be "Yes" or "No"')

        return yes_or_no


class RequestWorkflowSchema(BaseModel):
    name: str
    status: str
    nodes: Optional[list[NodeSchema]]

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
