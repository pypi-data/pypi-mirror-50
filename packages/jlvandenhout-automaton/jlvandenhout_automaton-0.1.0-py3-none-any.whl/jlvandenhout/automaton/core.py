"""The core functionality of the automaton package."""
from jlvandenhout.graph import Graph
from jlvandenhout.graph import search


class Automaton:
    """An automaton implementation.

    Args:
        graph: The graph to step through.
        nodes: An iterable of nodes to start from.
        accept: An iterable of nodes to accept.
        follow: A callable accepting an edge and a 
            symbol, which should determine if an edge 
            should be followed (True), unconditionally 
            be followed (None) or not be followed (False).
    """

    def __init__(self, graph, nodes, accept, follow):
        """See class description."""
        self.graph = graph
        self.subgraph = Graph()
        self.accept = set(accept)
        self.follow = follow

        self.nodes = nodes

    def consume(self, symbols):
        """Consume an iterable of symbols and yield accepted nodes.

        Args:
            symbols: An iterable of symbols.
        
        Yields:
            A set of currently accepted nodes.
        """
        yield self.accept.intersection(self.nodes)

        for symbol in symbols:
            self.update(symbol)

            if self.nodes:
                yield self.accept.intersection(self.nodes)
            else:
                break

    def update(self, symbol):
        """Update the automaton according the symbol.

        Args:
            symbol: The symbol to update.
        """
        nodes = set()

        for state in self.subgraph.closure:
            for edge in self.graph.edges.after(state):
                if self.follow(edge, symbol):
                    nodes.add(edge.after)

        self.nodes = nodes

    @property
    def symbols(self):
        """The alphabet of this automaton."""
        return set(edge.get() for edge in self.graph.edges)

    @property
    def nodes(self):
        """The part of the graph this automaton is currently in."""
        return set(self.subgraph)

    @nodes.setter
    def nodes(self, nodes):
        self.subgraph = search(self.graph, nodes, self.follow)
