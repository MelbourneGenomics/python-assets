import networkx as nx
from asset import Asset
import queue
import typing


class Bundle:
    queue: queue.Queue
    graph: nx.DiGraph()

    def __init__(self, assets: typing.Iterable[Asset] = None):
        # Initialise state
        self.queue = queue.Queue()
        self.graph = nx.DiGraph()

        # Add assets
        if assets is not None:
            for asset in assets:
                self.add_asset(asset)

    def add_asset(self, asset: Asset):
        node = self.graph.add_node(asset)
        for dependency in asset.dependencies:
            self.graph.add_edge(node, dependency)
        pass

    def build_queue(self):
        for node in nx.algorithms.topological_sort(self.graph):
            self.queue.put(node)
