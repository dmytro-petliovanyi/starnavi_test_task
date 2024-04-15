from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from ..db.models import Workflow
from ..db.repository import WorkflowRepository
from ..db.schemas import RequestWorkflowSchema, WorkflowSchema
from ..graphs.graph_create import WorkflowCreationService
from ..settings.configs import get_db
from ..settings.constants import IMAGE_FILE_PATH
from ..settings.exceptions import NodeCreationError
from .dependencies import (response_workflow_not_found,
                           response_workflow_not_valid)

workflow_router = APIRouter()


@workflow_router.post("/workflows", response_model=WorkflowSchema, status_code=status.HTTP_201_CREATED)
async def create_workflow(request: RequestWorkflowSchema, session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)

    name = request.name
    workflow_status = request.status
    nodes = request.nodes

    return await workflow_repo.create_workflow(name, workflow_status, nodes)


@workflow_router.put("/workflows/{workflow_id}", response_model=WorkflowSchema,
                     responses=response_workflow_not_found)
async def update_workflow(workflow_id: int,
                          request: RequestWorkflowSchema,
                          session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)
    workflow = await workflow_repo.get_single(workflow_id)

    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    new_name = request.name
    new_status = request.status
    nodes = request.nodes

    return await workflow_repo.update_workflow(workflow_id, new_name, new_status, nodes)


@workflow_router.delete("/workflows/{workflow_id}", response_model=dict[str, str],
                        responses=response_workflow_not_found)
async def delete_workflow(workflow_id: int,
                          session: Session = Depends(get_db)) -> dict[str, str]:
    workflow_repo = WorkflowRepository(session)
    workflow = await workflow_repo.get_single(workflow_id)

    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    await workflow_repo.delete_workflow(workflow_id)

    return {"message": "Workflow deleted successfully"}


@workflow_router.get("/workflows/{workflow_id}", response_model=WorkflowSchema,
                     responses=response_workflow_not_found)
async def get_workflow(workflow_id: int, session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)
    workflow = await workflow_repo.get_single(workflow_id)

    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    return workflow


@cache(expire=60)
@workflow_router.get("/workflows/{workflow_id}/draw",
                     responses=response_workflow_not_valid)
async def draw_workflow(workflow_id: int, session: Session = Depends(get_db)) -> FileResponse:
    service = WorkflowCreationService(session)

    try:
        workflow_graph = service.create_workflow_by_id(workflow_id)

    except NodeCreationError():
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Workflow is not valid")

    workflow_graph.get_graph()

    return FileResponse(IMAGE_FILE_PATH, media_type="image/png")
