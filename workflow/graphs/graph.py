import networkx as nx
from matplotlib import pyplot as plt

from workflow.settings.configs import logging
from workflow.settings.constants import IMAGE_FILE_PATH, NodeTypes, node_types
from workflow.settings.exceptions import EdgeCreationError, NodeCreationError


class WorkflowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: int, node_name: str, node_type: str, **kwargs) -> None:
        if node_type in node_types.keys():
            self.graph.add_node(node_id, node_type=node_type, node_name=node_name, **kwargs)
        else:
            raise NodeCreationError("No necessary keys")

    def add_edge(self, from_node: int, to_node: int, yes_or_no: str = "", weight: int = 2) -> None:
        if from_node in self.graph.nodes and to_node in self.graph.nodes:
            self.graph.add_edge(from_node, to_node, yes_or_no=yes_or_no, weight=weight)
        else:
            raise EdgeCreationError("Node doesn't exists")

    def validate_workflow(self) -> None:
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
                    except Exception as e:
                        logging.error(f"Error executing condition function for node {node_id}: {e}")
                    else:
                        for edge in self.graph.out_edges(node_id, data=True):
                            print(edge[2])
                            if condition_result:
                                if edge[2].get('yes_or_no') == "Yes":
                                    edge[2]['weight'] -= 1
                            if not condition_result:
                                if edge[2].get('yes_or_no') == "No":
                                    edge[2]['weight'] -= 1

    def get_graph(self):

        pos = nx.spring_layout(self.graph)
        edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        plt.savefig(IMAGE_FILE_PATH)
