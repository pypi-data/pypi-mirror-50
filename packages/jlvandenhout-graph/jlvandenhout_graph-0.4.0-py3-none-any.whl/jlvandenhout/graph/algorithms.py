"""Algorithms for the graph package."""

from collections import deque

from .structure import Graph


def search(graph, nodes, transition, depth_first=False):
    """Search the graph.

    The search starts from a set of nodes and applies the 
    transition function to every edge it finds. Both breadth 
    first and depth first searches can be used.

    Args:
        graph: The graph to search.
        nodes: The set of nodes to start searching from.
        transition: A function accepting an edge to 
            determine if the edge should be followed (True) 
            or not (False).
        depth_first: Search the graph depth or breadth first. 
            Defaults to False.
    
    Returns:
        A subgraph of graph, containing the found nodes and edges.
    
    Raises:
        NodeInvalid
    """
    subgraph = Graph()
    subgraph.nodes.add(*nodes)
    frontier = deque(nodes)

    while frontier:
        node = frontier.pop() if depth_first else frontier.popleft()

        for edge in graph.edges.succeeding(node):
            if edge.succeeding not in subgraph:
                if transition(edge):
                    subgraph.edges.update(edge.preceding, edge.succeeding, edge.value)
                    frontier.append(edge.succeeding)

    return subgraph
