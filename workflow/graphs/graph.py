import networkx as nx

from workflow.settings.configs import logging
from workflow.settings.constants import NodeTypes, node_types
from workflow.settings.exceptions import EdgeCreationError, NodeCreationError


class WorkflowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: int, node_name: str, node_type: str, **kwargs):
        if node_type in node_types and node_types.get(node_type) == kwargs:
            self.graph.add_node(node_id, node_type=node_type, node_name=node_name, **kwargs)
        raise NodeCreationError("No necessary keys")

    def add_edge(self, from_node: int, to_node: int, yes_or_no: str = "", weight: int = 2):
        if from_node in self.graph.nodes and to_node in self.graph.nodes:
            self.graph.add_edge(from_node, to_node, yes_or_no=yes_or_no, weight=weight)
        raise EdgeCreationError("Node doesn't exists")

    def validate_workflow(self):
        for node_id, data in self.graph.nodes(data=True):
            node_type = data.get('node_type')
            outgoing_edges = list(self.graph.successors(node_id))
            incoming_edges = list(self.graph.predecessors(node_id))

            if node_type == NodeTypes.START.value:
                if len(outgoing_edges) != 1:
                    raise NodeCreationError("Start node must have exactly one outgoing edge")
                if len(incoming_edges) != 0:
                    raise NodeCreationError("Start node cannot have incoming edges")
            elif node_type == NodeTypes.MESSAGE.value:
                if len(outgoing_edges) != 1:
                    raise NodeCreationError("Message node must have exactly one outgoing edge")
            elif node_type == NodeTypes.CONDITION.value:
                if len(outgoing_edges) != 2:
                    raise NodeCreationError("Condition node must have exactly two outgoing edges")
                if len(incoming_edges) == 0:
                    raise NodeCreationError("Condition node must have at least one incoming edge")
                for edge in outgoing_edges:
                    if "yes_or_no" not in self.graph.edges[node_id, edge]:
                        raise NodeCreationError("Edges for condition node must have yes_or_no attribute")
            elif node_type == NodeTypes.END.value:
                if len(incoming_edges) == 0:
                    raise NodeCreationError("End node must have at least one incoming edge")
                if len(outgoing_edges) != 0:
                    raise NodeCreationError("End node cannot have outgoing edges")

    def execute_workflow_with_condition(self):
        condition_results = {}

        for node_id in nx.topological_sort(self.graph):
            node_data = self.graph.nodes[node_id]

            if node_data['node_type'] == NodeTypes.CONDITION.value:
                incoming_edges = list(self.graph.in_edges(node_id))

                if incoming_edges:
                    last_message_node_id = incoming_edges[-1][0]
                    condition_string = node_data['condition']
                    eval_globals = {'prev_message_id': last_message_node_id}

                    try:
                        condition_result = eval(condition_string, eval_globals)
                        condition_results[node_id] = condition_result
                    except Exception as e:
                        logging.error(f"Error executing condition function for node {node_id}: {e}")

            else:
                if all(edge[0] in condition_results for edge in self.graph.in_edges(node_id)):
                    logging.info(f"Executing node {node_id} based on condition result: {condition_results}")
