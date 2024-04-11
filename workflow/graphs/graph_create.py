from workflow.db.repository import (ConditionRepository, EdgeRepository,
                                    EndNodeRepository, MessageNodeRepository,
                                    StartNodeRepository, WorkflowRepository)
from workflow.graphs.graph import WorkflowGraph


class WorkflowCreationService:
    def __init__(self, session):
        self.workflow_repo = WorkflowRepository(session)
        self.start_node_repo = StartNodeRepository(session)
        self.message_node_repo = MessageNodeRepository(session)
        self.condition_repo = ConditionRepository(session)
        self.end_node_repo = EndNodeRepository(session)
        self.edge_repo = EdgeRepository(session)

    def create_workflow_by_id(self, workflow_id):
        workflow = self.workflow_repo.get_single(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found.")

        node_ids = [node.id for node in workflow.nodes]

        workflow_graph = WorkflowGraph()

        for node_id in node_ids:
            node = self.start_node_repo.get_single(node_id)
            if not node:
                node = self.message_node_repo.get_single(node_id)
                if not node:
                    node = self.condition_repo.get_single(node_id)
                    if not node:
                        node = self.end_node_repo.get_single(node_id)
                        if not node:
                            raise ValueError(f"Node with ID {node_id} not found.")

            workflow_graph.add_node(node.id, node.name, node.node_type)

        edges = self.edge_repo.get()
        for edge in edges:
            workflow_graph.add_edge(edge.node_id, edge.next_node_id, yes_or_no=edge.yes_or_no)

        workflow_graph.validate_workflow()

        return workflow_graph
