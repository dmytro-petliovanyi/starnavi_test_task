from sqlalchemy import event
from sqlalchemy.orm import Session

from workflow.db.models import Node, Workflow


@event.listens_for(Node, 'after_delete')
def update_workflow_status(mapper, connection, node: Node):
    session = Session.object_session(node)
    workflow = session.query(Workflow).filter(Workflow.nodes.any(id=node.id)).first()

    if not all(workflow.nodes):
        workflow.status = 'No necessary node'
        session.commit()
