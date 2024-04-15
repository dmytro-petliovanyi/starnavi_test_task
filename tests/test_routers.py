from unittest.mock import patch

from fastapi import status

from tests.conftest import client, mock_workflows


@patch("workflow.routers.workflow.WorkflowRepository.create_workflow", return_value=mock_workflows[0])
def test_create_workflow(create_mock):
    response = client.post("/workflows", json=mock_workflows[0])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1, "name": "Math", "status": "some", "nodes": []}

    create_mock.assert_called_once()


@patch("workflow.routers.workflow.WorkflowRepository.get_single", return_value=mock_workflows[0])
def test_get_single_course(get_mock):
    response = client.get("/courses/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Math", "status": "some", "nodes": []}

    get_mock.assert_called_once()


@patch("workflow.routers.workflow.WorkflowRepository.update_workflow", return_value=mock_workflows[0])
@patch("workflow.routers.workflow.WorkflowRepository.get_single", return_value=mock_workflows[0])
def test_update_course(update_mock, get_mock):
    response = client.put("/courses/1", json=mock_workflows[0])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "course_name": "Math", "description": "some"}

    update_mock.assert_called_once()
    get_mock.assert_called_once()


@patch("workflow.routers.workflow.WorkflowRepository.delete_workflow")
@patch("workflow.routers.workflow.WorkflowRepository.get_single", return_value=mock_workflows[0])
def test_delete_course(delete_mock, not_found_mock):
    response = client.delete("/courses/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Workflow deleted successfully"}

    delete_mock.assert_called_once()
    not_found_mock.assert_called_once()
