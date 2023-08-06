"""An implementation of a graph."""


class Graph:
    """Methods to manipulate a graph."""

    def __init__(self):
        """See class documentation."""
        self.data = dict()

    @property
    def nodes(self):
        """Manipulate nodes."""
        return Nodes(self.data)

    @property
    def edges(self):
        """Manipulate edges."""
        return Edges(self.data)

    @property
    def closure(self):
        """Yield nodes in the closure set."""
        yield from (before for before, after in self.data.items() if not after)


class Nodes:
    """Methods to manipulate a graph by its nodes."""

    def __init__(self, data):
        """See class documentation."""
        self.data = data

    def add(self, node):
        """Add a node."""
        self.data.setdefault(node, dict())

    def remove(self, node):
        """Remove a node and all its edges."""
        for before in self.before(node):
            del self.data[before][node]
        del self.data[node]

    def before(self, node):
        """Yield all nodes before a node."""
        for before in self.data:
            if node in self.data[before]:
                yield before

    def after(self, node):
        """Yield all nodes after a node."""
        yield from self.data[node]

    def __iter__(self):
        yield from self.data


class Edges:
    """Methods to manipulate a graph by its edges."""

    def __init__(self, data):
        """See class documentation."""
        self.data = data

    def add(self, edge):
        """Add an edge."""
        self.set(*edge, edge.get())

    def remove(self, edge):
        """Remove an edge."""
        self.unset(*edge)

    def get(self, before, after):
        """Get the value of an edge."""
        return self.data[before][after]

    def set(self, before, after, value=None):
        """Set the value of an edge."""
        self.data.setdefault(before, dict())
        self.data.setdefault(after, dict())
        self.data[before][after] = value

    def unset(self, before, after):
        """Remove the edge between two nodes."""
        del self.data[before][after]

    def before(self, node):
        """Yield all edges before a node."""
        for before in self.data:
            if node in self.data[before]:
                yield Edge(self, before, node)

    def after(self, node):
        """Yield all edges after a node."""
        for after in self.data[node]:
            yield Edge(self, node, after)

    def __iter__(self):
        for before in self.data:
            for after in self.data[before]:
                yield Edge(self, before, after)


class Edge:
    """A proxy class representing an edge in the graph.
    
    Attributes:
        edges: An Edges instance.
        before: The node before this edge.
        after: The node after this edge.
    """

    def __init__(self, edges, before, after):
        """See class documentation."""
        self._edges = edges
        self._before = before
        self._after = after

    def get(self):
        """Return the value of this edge."""
        return self._edges.get(*self)

    def set(self, value=None):
        """Update the value of this edge."""
        self._edges.set(*self, value)

    def unset(self):
        """Remove this edge."""
        self._edges.unset(*self)

    @property
    def before(self):
        """The node before this edge."""
        return self._before

    @before.setter
    def before(self, node):
        value = self.get()
        self.unset()
        self._before = node
        self.set(value)

    @property
    def after(self):
        """The node after this edge."""
        return self._after

    @after.setter
    def after(self, node):
        value = self.get()
        self.unset()
        self._after = node
        self.set(value)

    def __iter__(self):
        yield self._before
        yield self._after
