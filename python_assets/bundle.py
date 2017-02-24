import networkx as nx
from asset import Asset
import queue
import typing
import multiprocessing


class Bundle:
    queue: list
    graph: nx.DiGraph

    def __init__(self, assets: typing.Iterable[Asset] = None):
        # Initialise state
        self.queue = []
        self.graph = nx.DiGraph()

        # Add assets
        if assets is not None:
            for asset in assets:
                self.add_asset(asset)

    def add_asset(self, asset: Asset):
        # Add both functions as nodes
        node = asset.id
        self.graph.add_node(node, asset=asset)

        for dependency in asset.dependencies:
            self.graph.add_edge(dependency, node)

    def build_queue(self):
        self.queue = nx.algorithms.topological_sort(self.graph, reverse=True)

    def install(self):
        """
        Runs the install process
        :return:
        """
        self.build_queue()
        self.execute_available()

    def execute_available(self):
        """
        Runs a subprocess for each available task
        :return:
        """
        executing = {}

        while self.queue:
            while self.queue:
                # Get the last element (the first in the queue)
                tail = self.queue[-1]

                # If there no dependencies to go, run this task
                if self.graph.predecessors(tail):
                    break
                else:
                    # Remove it from the queue since we know we're about to run it
                    self.queue.pop()

                    # Run the process
                    p = multiprocessing.Process(target=self.graph.node[tail]['asset'].execute)
                    p.start()

                    # Keep track of the node associated with the process
                    executing[tail] = p

            # Wait for them all to complete
            for node, process in list(executing.items()):
                process.join()
                del executing[node]
                self.graph.remove_node(node)
