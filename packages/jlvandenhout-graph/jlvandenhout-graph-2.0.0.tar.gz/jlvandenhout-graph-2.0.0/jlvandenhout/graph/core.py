"""An implementation of a graph."""

from collections.abc import Iterable
from collections.abc import Sized


class Base(Iterable):
    """Base class providing basic namespace functionality."""

    def __init__(self, data=None):
        """See class documentation."""
        self.data = dict() if data is None else data

    @property
    def graph(self):
        """Manipulate the graph."""
        return Graph(self.data)

    @property
    def nodes(self):
        """Manipulate nodes."""
        return Nodes(self.data)

    @property
    def edges(self):
        """Manipulate edges."""
        return Edges(self.data)

    def __iter__(self):
        yield from self.data


class Graph(Sized, Base):
    """Methods to manipulate a graph."""

    def reverse(self):
        """Reverse the edges."""
        self.edges.reverse()

    @property
    def closure(self):
        """Yield nodes in the closure set."""
        yield from (before for before, after in self.data.items() if not after)

    def __len__(self):
        return len(self.data)


class Nodes(Sized, Base):
    """Methods to manipulate a graph by its nodes."""

    def before(self, node):
        """Yield all nodes before a node."""
        for before, after in self.data.items():
            if node in after:
                yield before

    def after(self, node):
        """Yield all nodes after a node."""
        yield from self.data[node]

    def add(self, node):
        """Add a node."""
        self.data.setdefault(node, dict())

    def remove(self, node):
        """Remove a node and all its edges."""
        for before in self.before(node):
            del self.data[before][node]
        del self.data[node]

    def __len__(self):
        return len(self.data)


class Edges(Sized, Base):
    """Methods to manipulate a graph by its edges."""

    def get(self, before, after):
        """Get the value of an edge."""
        return self.data[before][after]

    def set(self, before, after, value=None):
        """Set the value of an edge."""
        self.nodes.add(before)
        self.nodes.add(after)
        self.data[before][after] = value

    def unset(self, before, after):
        """Remove the edge between two nodes."""
        del self.data[before][after]

    def before(self, node):
        """Yield all edges before a node."""
        for before in self.nodes:
            if node in self.nodes.after(before):
                yield Edge(before, node, data=self.data)

    def after(self, node):
        """Yield all edges after a node."""
        for after in self.nodes.after(node):
            yield Edge(node, after, data=self.data)

    def add(self, edge):
        """Add an edge."""
        self.set(*edge, edge.get())

    def remove(self, edge):
        """Remove an edge."""
        self.unset(*edge)

    def reverse(self):
        """Reverse the edges."""
        for edge in list(self):
            edge.reverse()

    def __iter__(self):
        for before in self.nodes:
            for after in self.nodes.after(before):
                yield Edge(before, after, data=self.data)

    def __len__(self):
        return sum(map(len, self.data.values()))


class Edge(Base):
    """A proxy class representing an edge in the graph.
    
    Args:
        before: The node before this edge.
        after: The node after this edge.
        data: The data referenced.
    """

    def __init__(self, before, after, value=None, data=None):
        """See class documentation."""
        super().__init__(data)
        self._before = before
        self._after = after

        if not data:
            self.set(value)

    def get(self):
        """Return the value of this edge."""
        return self.edges.get(*self)

    def set(self, value=None):
        """Update the value of this edge."""
        self.edges.set(*self, value)

    def unset(self):
        """Remove this edge."""
        self.edges.unset(*self)

    def remove(self):
        """Remove this edge."""
        self.edges.remove(self)

    def reverse(self):
        """Reverse this edge."""
        value = self.get()
        self.unset()
        self._before, self._after = self._after, self._before
        self.set(value)

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
