from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from workflow.settings.configs import Base


class Node(Base):
    __tablename__ = 'nodes'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    node_type: str = Column(String(20), nullable=False)

    next_nodes = relationship('Edge',
                              back_populates='previous_node',
                              cascade='all, delete-orphan')

    previous_nodes = relationship('Edge',
                                  back_populates='next_node',
                                  cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f"{self.name} {self.node_type}"


class Edge(Base):
    __tablename__ = 'edges'
    id: int = Column(Integer, primary_key=True)
    node_id: int = Column(Integer, ForeignKey('nodes.id'))
    next_node_id: int = Column(Integer, ForeignKey('nodes.id'))
    yes_or_no: str = Column(String(255))

    previous_node = relationship('Node', back_populates='next_nodes', foreign_keys="node_id")
    next_node = relationship('Node', back_populates='previous_nodes', foreign_keys="next_node_id")

    def __str__(self) -> str:
        return str(self.node_id)


class Workflow(Base):
    __tablename__ = 'workflows'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    status: str = Column(String(255))

    nodes = relationship('Node', back_populates='workflow')

    def __str__(self) -> str:
        return f"{self.name}; status: {self.status}"


class StartNode(Node):
    __tablename__ = 'start_nodes'


class MessageNode(Node):
    __tablename__ = 'message_nodes'
    status: str = Column(String(255))
    message: str = Column(String(255))


class ConditionNode(Node):
    __tablename__ = 'condition_nodes'
    condition: str = Column(String(255))


class EndNode(Node):
    __tablename__ = 'end_nodes'


all_models = [Edge, Workflow, StartNode, MessageNode, ConditionNode, EndNode, Node]
