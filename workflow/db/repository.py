from sqlalchemy.orm import Session

from workflow.db.models import (ConditionNode, Edge, EndNode, MessageNode,
                                Node, StartNode, Workflow, all_models)
from workflow.settings.configs import Base
from workflow.settings.constants import NodeTypes


class BaseRepository:
    model = Base

    def __init__(self, session: Session):
        self.session = session

    async def get(self) -> list[Base]:
        async with self.session as async_session:
            result = await async_session.execute(self.model)
            return result.scalars().all()

    async def get_single(self, row_id: int) -> Base | None:
        async with self.session as async_session:
            result = await async_session.execute(self.model.filter_by(id=row_id))
            return result.scalar_one_or_none()


class WorkflowRepository(BaseRepository):
    model = all_models[1]

    async def create_workflow(self,
                              name: str,
                              status: str,
                              nodes: list[Node]) -> Workflow:
        async with self.session as async_session:
            workflow = self.model(name=name, status=status, nodes=nodes)
            async_session.add(workflow)
            await async_session.commit()
            return workflow

    async def update_workflow(self,
                              workflow_id: int,
                              new_name: str,
                              new_status: str,
                              nodes: list[StartNode | EndNode | MessageNode | ConditionNode]) -> Workflow:
        async with self.session as async_session:
            workflow = await async_session.get(self.model, workflow_id)
            if workflow:
                workflow.name = new_name
                workflow.status = new_status
                workflow.nodes = nodes
                await async_session.commit()
            return workflow

    async def delete_workflow(self, workflow_id: int) -> None:
        async with self.session as async_session:
            workflow = await async_session.get(self.model, workflow_id)
            if workflow:
                async_session.delete(workflow)
                await async_session.commit()


class EdgeRepository(BaseRepository):
    model = all_models[0]

    async def get_by_node(self, node_id: int) -> list[Edge] | None:
        async with self.session as async_session:
            result = await async_session.execute(self.model.filter_by(node_id=node_id))
            return result.scalars().all()

    async def delete_edge(self, edge_id: int) -> None:
        async with self.session as async_session:
            edge = await async_session.get(self.model, edge_id)
            if edge:
                async_session.delete(edge)
                await async_session.commit()

    async def update_edge(self,
                          edge_id: int,
                          new_node_id: int,
                          new_next_node_id: int,
                          yes_or_no: str = "") -> Edge | None:
        async with self.session as async_session:
            edge = await async_session.get(self.model, edge_id)
            if edge:
                edge.node_id = new_node_id
                edge.next_node_id = new_next_node_id
                edge.yes_or_no = yes_or_no
                await async_session.commit()
            return edge

    async def create_edge(self, node_id: int, next_node_id: int, yes_or_no: str = "") -> Edge | None:
        async with self.session as async_session:
            edge = self.model(node_id=node_id, next_node_id=next_node_id, yes_or_no=yes_or_no)
            async_session.add(edge)
            await async_session.commit()
            return edge


class NodeRepositoryBase(BaseRepository):
    model = all_models[6]
    node_type = "BaseNode"

    async def get_single(self, node_id: int, node_type: str = None) -> StartNode | None:
        async with self.session as async_session:
            if node_type:
                result = await async_session.execute(self.model.filter_by(node_id=node_id, node_type=node_type))
            else:
                result = await async_session.execute(self.model.filter_by(node_id=node_id))
            return result.scalar_one_or_none()

    async def delete_node(self, node_id: int) -> None:
        async with self.session as async_session:
            node = await async_session.get(self.model, node_id)
            if node:
                async_session.delete(node)
                await async_session.commit()

    async def update_node(self, node_id: int, new_name: str) -> StartNode | None:
        async with self.session as async_session:
            node = await async_session.get(self.model, node_id)
            if node:
                node.name = new_name
                await async_session.commit()
            return node

    async def create_node(self, name: str) -> ConditionNode:
        async with self.session as async_session:
            node = self.model(name=name, node_type=self.node_type)
            async_session.add(node)
            await async_session.commit()
            return node


class StartNodeRepository(NodeRepositoryBase):
    model = all_models[2]
    node_type = NodeTypes.START.value


class EndNodeRepository(NodeRepositoryBase):
    model = all_models[5]
    node_type = NodeTypes.END.value


class MessageNodeRepository(NodeRepositoryBase):
    model = all_models[3]
    node_type = NodeTypes.MESSAGE.value

    async def update_node(self, node_id: int, new_name: str, new_status: str, new_message: str) -> MessageNode | None:
        async with self.session as async_session:
            node = await async_session.get(self.model, node_id)

            if node:
                node.name = new_name
                node.status = new_status
                node.message = new_message
                await async_session.commit()
                return node

    async def create_node(self, name: str, status: str, message: str) -> MessageNode:
        async with self.session as async_session:
            node = self.model(name=name, status=status, message=message, node_type=self.node_type)
            async_session.add(node)
            await async_session.commit()
            return node


class ConditionNodeRepository(NodeRepositoryBase):
    model = all_models[4]
    node_type = NodeTypes.CONDITION.value

    async def update_node(self, node_id: int, new_name: str, condition: str) -> ConditionNode | None:
        async with self.session as async_session:
            node = await async_session.get(self.model, node_id)

            if node:
                node.name = new_name
                node.condition = condition
                await async_session.commit()
                return node

    async def create_node(self, name: str, status: str, condition: str) -> ConditionNode:
        async with self.session as async_session:
            node = self.model(name=name, status=status, node_type=self.node_type, condition=condition)
            async_session.add(node)
            await async_session.commit()
            return node
