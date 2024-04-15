import pytest

from workflow.settings.constants import NodeTypes
from workflow.settings.exceptions import NodeCreationError


def test_add_node(workflow_graph):
    workflow_graph.add_node(1, "Start", NodeTypes.START.value)
    workflow_graph.add_node(2, "Message 1", NodeTypes.MESSAGE.value, status="OPEN", message="some")
    workflow_graph.add_node(3, "Condition", NodeTypes.CONDITION.value, condition="prev_message_id > 0")
    workflow_graph.add_node(4, "End", NodeTypes.END.value)

    assert len(workflow_graph.graph.nodes) == 4


def test_add_edge(workflow_graph):
    workflow_graph.add_node(1, "Start", NodeTypes.START.value)
    workflow_graph.add_node(2, "Message 1", NodeTypes.MESSAGE.value, status="OPEN", message="some")
    workflow_graph.add_edge(1, 2)

    assert workflow_graph.graph.has_edge(1, 2)


def test_validate_workflow(workflow_graph):
    workflow_graph.add_node(1, "Start", NodeTypes.START.value)
    workflow_graph.add_node(2, "Message 1", NodeTypes.MESSAGE.value)
    workflow_graph.add_node(3, "Condition", NodeTypes.CONDITION.value, condition="prev_message_id > 0")

    with pytest.raises(NodeCreationError):
        workflow_graph.validate_workflow()

    workflow_graph.add_node(4, "End", NodeTypes.END.value)
    workflow_graph.add_node(5, "End2", NodeTypes.END.value)
    workflow_graph.add_edge(1, 2)
    workflow_graph.add_edge(2, 3)
    workflow_graph.add_edge(3, 4, yes_or_no="yes")
    workflow_graph.add_edge(3, 5, yes_or_no="no")

    workflow_graph.validate_workflow()


def test_execute_workflow_with_condition(workflow_graph):
    workflow_graph.add_node(1, "Start", NodeTypes.START.value)
    workflow_graph.add_node(2, "Message 1", NodeTypes.MESSAGE.value)
    workflow_graph.add_node(3, "Condition", NodeTypes.CONDITION.value, condition="True")
    workflow_graph.add_node(4, "End", NodeTypes.END.value)
    workflow_graph.add_node(5, "END2", NodeTypes.END.value)
    workflow_graph.add_edge(1, 2)
    workflow_graph.add_edge(2, 3)
    workflow_graph.add_edge(3, 4, yes_or_no="Yes")
    workflow_graph.add_edge(3, 5, yes_or_no="No")
    workflow_graph.execute_workflow_with_condition()
