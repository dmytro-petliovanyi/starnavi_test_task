from unittest.mock import patch

from workflow.db.repository import WorkflowRepository


async def test_workflow_repository_get_single(override_dependency, override_get_db, prepare_db, mock_workflow):
    async with override_get_db() as session:
        workflow_repo = WorkflowRepository(session)

        workflow_repo.session.add(mock_workflow)
        workflow_repo.session.commit()

        assert mock_workflow == workflow_repo.get_single(1)


async def test_workflow_repository_create_workflow(override_dependency, override_get_db, prepare_db, mock_workflow):
    async with override_get_db() as session:
        workflow_repo = WorkflowRepository(session)

        new_workflow = mock_workflow
        workflow = workflow_repo.create_workflow(name="New Workflow", status="Active", nodes=[])
        assert new_workflow.name == workflow.name
        assert new_workflow.status == workflow.status


@patch("workflow.db.repository.WorkflowRepository.get_single")
async def test_workflow_repository_delete_workflow(get_single_mock, override_dependency,
                                                   override_get_db, prepare_db, mock_workflow):
    async with override_get_db() as session:
        workflow_repo = WorkflowRepository(session)

        workflow_repo.session.add(mock_workflow)
        workflow_repo.session.commit()

        get_single_mock.return_value = mock_workflow

        workflow_id = 1
        result = workflow_repo.delete_workflow(workflow_id=1)

        assert result is None
        assert workflow_repo.session.query(workflow_repo.model).filter_by(id=1).first() is None

        get_single_mock.assert_called_once_with(workflow_id)
