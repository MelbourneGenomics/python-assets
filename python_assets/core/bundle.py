import pathlib
from multiprocessing import Pipe
from pkg_resources import resource_string
from python_assets.core.asset import Asset
import typing
import multiprocessing


class Bundle:
    order: typing.List[Asset]
    """A queue of assets to install, where the last item in the list is the first to be installed"""

    assets: typing.Dict[str, Asset]
    """A dictionary of all assets in this bundle, mapping asset id to asset object"""

    directory: pathlib.Path
    """The root of the asset bundle. All assets are installed relative to here."""

    def __init__(self, directory: pathlib.Path, assets: typing.Iterable[Asset] = None):
        self.order = []
        self.assets = {}
        self.directory = directory

        # Add assets
        if assets is not None:
            for asset in assets:
                self.add_asset(asset)

    def generate_environment(self):
        env_file = self.directory / 'environment'
        env_file.write_bytes(resource_string('python_assets', 'environment.sh'))

    def add_asset(self, asset: Asset):
        """
        Add an asset to the bundle
        :param asset:
        """
        # Add the asset node
        self.assets[asset.id] = asset

        # Tell the asset about this bundle
        asset.bundle = self

    def build_queue(self):
        """
        Internal method. Adds edges to the nodes and builds a topographically sorted list of edges
        """
        # Add the graph edges
        for id, asset in self.assets.items():
            for dependency_id in asset.dependency_ids:
                dependency = self.assets[dependency_id]
                dependency.add_dependent(asset)

        # Topological sort to produce a list of jobs
        for id, asset in self.assets.items():
            self.visit_node(asset)

    def visit_node(self, node: Asset):
        """Internal method. Used in topographically sorting the asset nodes"""
        if node.visited:
            return

        node.visited = True

        for dependent in node.dependents:
            self.visit_node(dependent)

        self.order.append(node)

    def install(self, create_env: bool = False):
        """
        Runs the install process
        """
        self.build_queue()
        self.execute_available()
        if create_env:
            self.generate_environment()

    def execute_available(self):
        """
        Internal method. Runs a subprocess for each available task
        """
        executing = {}

        # Keep looping until everything is done
        while self.order or executing:

            # If the last element in the array has no dependencies to go, run this task
            if self.order and self.order[-1].deps_satisfied:

                # Remove it from the queue since we know we're about to run it
                tail = self.order.pop()

                # Provide a communication channel
                parent, child = Pipe()

                # Run the process
                proc = multiprocessing.Process(target=tail.execute, args=(child,))

                proc.start()

                # Keep track of the node associated with the process
                executing[tail] = (proc, parent)

            # Otherwise if we've started all the assets we can, just wait for them to complete
            else:
                # Wait for them all to complete
                for node, (process, parent) in list(executing.items()):
                    # Wait for this process to complete
                    process.join()

                    # When it does, read the start, finish times
                    node.piped = parent.recv()

                    # Update its dependent tasks
                    node.complete()

                    # Stop tracking it
                    del executing[node]
