"""Algorithms for the graph package."""

from collections import deque

from .core import Graph


def search(graph, nodes, follow, depth_first=False):
    """Search a graph.

    The search starts from a set of nodes and applies the 
    follow function to every edge it finds. Both breadth 
    first and depth first searches can be used.

    Args:
        graph: The graph to search.
        nodes: The set of nodes to start searching from.
        follow: A function accepting an edge to 
            determine if the edge should be followed (True), 
            unconditionally be followed (None) or not be 
            followed (False).
        depth_first: Search the graph depth or breadth first. 
            Defaults to False.
    
    Returns:
        A subgraph of graph, containing the found nodes and edges.
    
    Raises:
        NodeInvalid
    """
    frontier = deque()
    subgraph = Graph()

    for node in nodes:
        frontier.append(node)
        subgraph.nodes.add(node)

    while frontier:
        node = frontier.pop() if depth_first else frontier.popleft()

        for edge in graph.edges.after(node):
            if edge.after not in subgraph:
                if follow(edge) is not False:
                    subgraph.edges.add(edge)
                    frontier.append(edge.after)

    return subgraph
