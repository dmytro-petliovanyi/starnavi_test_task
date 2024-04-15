from typing import Any

from fastapi import status
from sqlalchemy.orm import Session

from workflow.db.repository import (ConditionNodeRepository, EndNodeRepository,
                                    MessageNodeRepository, NodeRepositoryBase,
                                    StartNodeRepository)
from workflow.db.schemas import DefaultResponseModel, RequestNodeSchema
from workflow.settings.constants import NodeTypes


async def pick_node_repository(node_type: str, session: Session) -> NodeRepositoryBase:
    if node_type == NodeTypes.START.value:
        return StartNodeRepository(session)
    if node_type == NodeTypes.END.value:
        return EndNodeRepository(session)
    if node_type == NodeTypes.MESSAGE.value:
        return MessageNodeRepository(session)
    if node_type == NodeTypes.CONDITION.value:
        return ConditionNodeRepository(session)

    raise ValueError(f"{node_type} not in available node types")


async def get_values_from_request(request: RequestNodeSchema, node_type: str):
    attributes = {"name": request.name, "node_type": request.node_type}

    if node_type == NodeTypes.MESSAGE.value:
        attributes["status"] = request.status
        attributes["message"] = request.message

    if node_type == NodeTypes.CONDITION.value:
        attributes["condition"] = request.condition

    return attributes


async def pick_node_repository_by_node_id(node_id: int,
                                          session: Session) -> NodeRepositoryBase | None:
    general_node = await NodeRepositoryBase(session).get_single(node_id)
    node_type = general_node.node_type

    node_repo_typed = pick_node_repository(node_type, session)

    return node_repo_typed

response_workflow_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": "Workflow not found"
    }
}

response_node_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": "Node not found"
    }
}

response_edge_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": "Edge not found"
    }
}


response_workflow_not_valid: dict[int | str, dict[str, Any]] = {
    status.HTTP_501_NOT_IMPLEMENTED: {
              "model": DefaultResponseModel,
              "description": "Workflow is not valid"
    }
}
