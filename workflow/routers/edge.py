from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from workflow.db.models import Edge
from workflow.db.repository import EdgeRepository
from workflow.db.schemas import EdgeSchema, RequestEdgeSchema
from workflow.routers.dependencies import response_edge_not_found
from workflow.settings.configs import get_db

edge_router = APIRouter()


@edge_router.post("/edges", response_model=EdgeSchema, status_code=status.HTTP_201_CREATED)
async def create_edge(request: RequestEdgeSchema,
                      session: Session = Depends(get_db)) -> Edge:
    edge_repo = EdgeRepository(session)

    node_id = request.node_type
    next_node_id = request.node_type
    yes_or_no = request.yes_or_no if request.yes_or_no else ""

    return await edge_repo.create_edge(node_id, next_node_id, yes_or_no)


@edge_router.put("/edges/{edge_id}", response_model=EdgeSchema,
                 responses=response_edge_not_found)
async def update_edge(edge_id: int,
                      request: RequestEdgeSchema,
                      session: Session = Depends(get_db)) -> Edge:
    edge_repo = EdgeRepository(session)
    edge = await edge_repo.get_single(edge_id)

    if edge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    node_id = request.node_type
    next_node_id = request.node_type
    yes_or_no = request.yes_or_no if request.yes_or_no else ""

    return await edge_repo.update_edge(edge_id, node_id, next_node_id, yes_or_no)


@edge_router.delete("/edges/{edge_id}", response_model=dict[str, str],
                    responses=response_edge_not_found)
async def delete_edge(edge_id: int,
                      session: Session = Depends(get_db)) -> dict[str, str]:
    edge_repo = EdgeRepository(session)
    edge = await edge_repo.get_single(edge_id)

    if edge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    await edge_repo.delete_edge(edge_id)

    return {"message": "Workflow deleted successfully"}


@edge_router.get("/edges/{edge_id}", response_model=EdgeSchema,
                 responses=response_edge_not_found)
async def get_edge(edge_id: int,
                   session: Session = Depends(get_db)) -> Edge:
    edge_repo = EdgeRepository(session)
    edge = await edge_repo.get_single(edge_id)

    if edge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

    return edge
