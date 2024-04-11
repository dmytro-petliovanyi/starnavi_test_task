from sqlalchemy.orm import Session

from workflow.db.models import (ConditionNode, Edge, MessageNode, Node,
                                StartNode, Workflow, all_models)


class WorkflowRepository:
    model = all_models[1]

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Workflow]:
        return self.session.query(self.model).all()

    def get_single(self, workflow_id: int) -> Workflow | None:
        return self.session.query(self.model).filter_by(id=workflow_id).first()

    def delete_workflow(self, workflow_id: int) -> None:
        workflow = self.get_single(workflow_id)
        if workflow:
            self.session.delete(workflow)
            self.session.commit()

    def update_workflow(self, workflow_id: int, new_name: str, new_status: str, node_ids: list[int]) -> Workflow | None:
        workflow = self.get_single(workflow_id)

        if workflow:
            workflow.name = new_name
            workflow.status = new_status
            workflow.nodes = [self.session.query(Node).filter_by(id=node_id).first() for node_id in node_ids]
            self.session.commit()
            return workflow

    def create_workflow(self, name: str, status: str, node_ids: list[int]) -> Workflow:
        workflow = self.model(name=name, status=status)
        workflow.nodes = [self.session.query(Node).filter_by(id=node_id).first() for node_id in node_ids]
        self.session.add(workflow)
        self.session.commit()
        return workflow


class EdgeRepository:
    model = all_models[0]

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Edge]:
        return self.session.query(self.model).all()

    def get_single(self, edge_id: int) -> Edge | None:
        return self.session.query(self.model).filter_by(id=edge_id).first()

    def delete_edge(self, edge_id: int) -> None:
        edge = self.get_single(edge_id)
        if edge:
            self.session.delete(edge)
            self.session.commit()

    def update_edge(self, edge_id: int, new_node_id: int, new_next_node_id: int, yes_or_no: str = "") -> Edge | None:
        edge = self.get_single(edge_id)

        if edge:
            edge.node_id = new_node_id
            edge.next_node_id = new_next_node_id
            edge.yes_or_no = yes_or_no
            self.session.commit()
            return edge

    def create_edge(self, node_id: int, next_node_id: int, yes_or_no: str = "") -> Edge:
        edge = self.model(node_id=node_id, next_node_id=next_node_id, yes_or_no=yes_or_no)
        self.session.add(edge)
        self.session.commit()
        return edge


class NodeRepositoryBase:
    model = all_models[6]
    node_type = "StartNode"

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[StartNode]:
        return self.session.query(self.model).all()

    def get_single(self, node_id: int, node_type: str = None) -> StartNode | None:
        if node_type:
            return self.session.query(self.model).filter_by(id=node_id, node_type=node_type).first()
        return self.session.query(self.model).filter_by(id=node_id).first()

    def delete_node(self, node_id: int) -> None:
        node = self.get_single(node_id)
        if node:
            self.session.delete(node)
            self.session.commit()

    def update_node(self, node_id: int, new_name: str) -> StartNode | None:
        node = self.get_single(node_id)

        if node:
            node.name = new_name
            self.session.commit()
            return node


class StartNodeRepository(NodeRepositoryBase):
    model = all_models[2]
    node_type = "StartNode"


class EndNodeRepository(NodeRepositoryBase):
    model = all_models[5]
    node_type = "EndNode"


class MessageNodeRepository(NodeRepositoryBase):
    model = all_models[3]
    node_type = "MessageNode"

    def update_node(self, node_id: int, new_name: str, new_status: str, new_message: str) -> MessageNode | None:
        node = self.get_single(node_id)

        if node:
            node.name = new_name
            node.status = new_status
            node.message = new_message
            self.session.commit()
            return node

    def create_node(self, name: str, status: str, message: str) -> MessageNode:
        node = self.model(name=name, status=status, message=message, node_type=self.node_type)
        self.session.add(node)
        self.session.commit()
        return node


class ConditionRepository(NodeRepositoryBase):
    model = all_models[4]
    node_type = "ConditionNode"

    def update_node(self, node_id: int, new_name: str, condition: str) -> ConditionNode | None:
        node = self.get_single(node_id)

        if node:
            node.name = new_name
            node.condition = condition
            self.session.commit()
            return node

    def create_node(self, name: str, status: str, condition: str) -> ConditionNode:
        node = self.model(name=name, status=status, node_type=self.node_type, condition=condition)
        self.session.add(node)
        self.session.commit()
        return node
