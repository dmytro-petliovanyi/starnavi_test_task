from workflow.db.models import Edge, Workflow
from workflow.db.repository import (EdgeRepository, NodeRepositoryBase,
                                    WorkflowRepository)
from workflow.graphs.graph import WorkflowGraph
from workflow.routers.dependencies import pick_node_repository_by_node_id


class WorkflowCreationService:
    def __init__(self, session):
        self.session = session
        self.workflow_repo = WorkflowRepository(session)
        self.node_repo = NodeRepositoryBase(session)
        self.edge_repo = EdgeRepository(session)

    async def create_workflow_by_id(self, workflow_id) -> WorkflowGraph:
        workflow = await self._get_workflow(workflow_id)
        node_ids = self.get_node_ids(workflow)
        workflow_edges = self._get_workflow_edges(node_ids)
        workflow_graph = self._create_workflow_graph(node_ids, workflow_edges)
        self.execute_workflow(workflow_graph)

        return workflow_graph

    async def _get_workflow(self, workflow_id) -> Workflow:
        workflow = await self.workflow_repo.get_single(workflow_id)

        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found.")

        return workflow

    async def _get_workflow_edges(self, node_ids) -> list[Edge]:
        workflow_edges = []

        for node_id in node_ids:
            node_edges = await self.edge_repo.get_by_node(node_id)
            workflow_edges.extend(node_edges)

        return workflow_edges

    async def _create_workflow_graph(self, node_ids, workflow_edges) -> WorkflowGraph:
        workflow_graph = WorkflowGraph()

        for node_id in node_ids:
            node_repo = pick_node_repository_by_node_id(node_id, self.session)
            node = await node_repo.get_single(node_id)
            workflow_graph.add_node(node.id, node.name, node.node_type)

        for edge in workflow_edges:
            workflow_graph.add_edge(edge.node_id, edge.next_node_id, yes_or_no=edge.yes_or_no)

        workflow_graph.validate_workflow()
        return workflow_graph

    @staticmethod
    def execute_workflow(workflow_graph):
        workflow_graph.execute_workflow_with_condition()

    @staticmethod
    def get_node_ids(workflow) -> list[int]:
        return [node.id for node in workflow.nodes]
