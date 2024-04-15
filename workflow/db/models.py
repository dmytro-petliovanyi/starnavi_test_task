from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from workflow.settings.configs import Base

workflow_node_association = Table(
    'workflow_node_association',
    Base.metadata,
    Column('workflow_id', Integer, ForeignKey('workflows.id')),
    Column('node_id', Integer, ForeignKey('nodes.node_id'))
)


class NodeMixin:
    id = Column(Integer, ForeignKey('nodes.node_id'), primary_key=True)
    name = Column(String(50), nullable=False)
    node_type = Column(String(20), nullable=False)

    def __str__(self):
        return f"{self.name} {self.node_type}"


class Node(Base):
    __tablename__ = 'nodes'
    node_id: int = Column(Integer, primary_key=True)
    node_type: str = Column(String(20))

    workflows = relationship('Workflow', secondary=workflow_node_association, back_populates='nodes')

    __mapper_args__ = {
        'polymorphic_identity': 'node',
        'polymorphic_on': node_type
    }


class Edge(Base):
    __tablename__ = 'edges'
    id: int = Column(Integer, primary_key=True)
    node_id: int = Column(Integer, ForeignKey('nodes.node_id'))
    next_node_id: int = Column(Integer, ForeignKey('nodes.node_id'))
    yes_or_no: str = Column(String(255))

    def __str__(self) -> str:
        return str(self.node_id)


class Workflow(Base):
    __tablename__ = 'workflows'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    status: str = Column(String(255))

    nodes = relationship('Node', secondary=workflow_node_association, back_populates='workflows')

    def __str__(self) -> str:
        return f"{self.name}; status: {self.status}"


class StartNode(Node, NodeMixin):
    __tablename__ = 'start_nodes'


class MessageNode(Node, NodeMixin):
    __tablename__ = 'message_nodes'
    status: str = Column(String(255))
    message: str = Column(String(255))


class ConditionNode(Node, NodeMixin):
    __tablename__ = 'condition_nodes'
    condition: str = Column(String(255))


class EndNode(Node, NodeMixin):
    __tablename__ = 'end_nodes'


all_models = [Edge, Workflow, StartNode, MessageNode, ConditionNode, EndNode, Node]
