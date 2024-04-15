from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from workflow.db.models import ConditionNode, EndNode, MessageNode, StartNode
from workflow.db.schemas import NodeSchema, RequestNodeSchema
from workflow.routers.dependencies import (get_values_from_request,
                                           pick_node_repository,
                                           pick_node_repository_by_node_id,
                                           response_node_not_found)
from workflow.settings.configs import get_db

node_router = APIRouter()


@node_router.post("/nodes", response_model=NodeSchema, status_code=status.HTTP_201_CREATED)
async def create_node(request: RequestNodeSchema,
                      session: Session = Depends(get_db)) -> StartNode | EndNode | MessageNode | ConditionNode:
    node_type = request.node_type
    node_repo = pick_node_repository(node_type, session)
    node_attr = get_values_from_request(request, node_type)

    node_attr.__delitem__("node_type")

    return await node_repo.create_node(**node_attr)


@node_router.put("/nodes/{node_id}", response_model=NodeSchema,
                 responses=response_node_not_found)
async def update_node(node_id: int,
                      request: RequestNodeSchema,
                      session: Session = Depends(get_db)) -> StartNode | EndNode | MessageNode | ConditionNode:
    node_repo = pick_node_repository_by_node_id(node_id, session)
    node = await node_repo.get_single(node_id)

    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    node_type = request.node_type
    node_attr = get_values_from_request(request, node_type)

    return await node_repo.update_node(node_id, **node_attr)


@node_router.delete("/nodes/{node_id}", response_model=dict[str, str],
                    responses=response_node_not_found)
async def delete_node(node_id: int,
                      session: Session = Depends(get_db)) -> dict[str, str]:
    node_repo = pick_node_repository_by_node_id(node_id, session)
    node = await node_repo.get_single(node_id)

    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    await node_repo.delete_node(node_id)

    return {"message": "Workflow deleted successfully"}


@node_router.get("/nodes/{node_id}", response_model=NodeSchema,
                 responses=response_node_not_found)
async def get_node(node_id: int,
                   session: Session = Depends(get_db)) -> StartNode | EndNode | MessageNode | ConditionNode:
    node_repo = pick_node_repository_by_node_id(node_id, session)
    node = await node_repo.get_single(node_id)

    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    return node
