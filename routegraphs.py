
from graphs import Node, Graph
import osmium as osm
import random

class RouteNode(Node):
    def __init__(self, node, value=None):
        self.node = node
        super().__init__(node.name, value)