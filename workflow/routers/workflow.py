from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from matplotlib import pyplot as plt
from sqlalchemy.orm import Session

from ..db.models import Workflow
from ..db.repository import WorkflowRepository
from ..db.schemas import RequestWorkflowSchema, WorkflowSchema
from ..graphs.graph_create import WorkflowCreationService
from ..settings.configs import get_db
from ..settings.exceptions import NodeCreationError

workflow_router = APIRouter()


@workflow_router.post("/workflows", response_model=WorkflowSchema, status_code=status.HTTP_201_CREATED)
async def create_workflow(request: RequestWorkflowSchema, session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)

    name = request.name
    workflow_status = request.status
    nodes = request.nodes

    return workflow_repo.create_workflow(name, workflow_status, nodes)


@workflow_router.put("/workflows/{workflow_id}", response_model=WorkflowSchema)
async def update_workflow(workflow_id: int,
                          request: RequestWorkflowSchema,
                          session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)
    workflow = workflow_repo.get_single(workflow_id)

    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    new_name = request.name
    new_status = request.status
    nodes = request.nodes

    return workflow_repo.update_workflow(workflow_id, new_name, new_status, nodes)


@workflow_router.delete("/workflows/{workflow_id}", response_model=dict[str, str])
async def delete_workflow(workflow_id: int,
                          session: Session = Depends(get_db)) -> dict[str, str]:
    workflow_repo = WorkflowRepository(session)
    db_workflow = workflow_repo.get_single(workflow_id)

    if db_workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    workflow_repo.delete_workflow(workflow_id)

    return {"message": "Workflow deleted successfully"}


@workflow_router.get("/workflows/{workflow_id}", response_model=WorkflowSchema)
async def get_workflow(workflow_id: int, session: Session = Depends(get_db)) -> Workflow:
    workflow_repo = WorkflowRepository(session)
    db_workflow = workflow_repo.get_single(workflow_id)

    if db_workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    return db_workflow


@workflow_router.get("/workflows/{workflow_id}/draw")
async def draw_workflow(workflow_id: int, session: Session = Depends(get_db)) -> FileResponse:
    service = WorkflowCreationService(session)
    workflow_graph = service.create_workflow_by_id(workflow_id)
    try:
        workflow_graph.validate_workflow()
    except NodeCreationError():
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Workflow is not valid")
    workflow_graph.execute_workflow_with_condition()
    plt.savefig("workflow_graph.png")
    return FileResponse("workflow_graph.png", media_type="image/png")
