class Node:

  def __init__(self, name, value=None):
    self.name = name
    self.value = value
    self.domain = set()

  def is_assigned(self):
    return self.value != None
    
  def assign(self, value):
    self.value = value

  def unassign(self):
    self.value = None

  def get_domain(self):
    return self.domain

  def __str__(self):
    return f"Node: {self.name} with value: {self.value}"

  def __lt__(self, other):
    return True
  
class Graph:
  def __init__(self):
    self.adj_list = {}
    self.nodes = {}

  def add_node(self, name, value=None):
    self.nodes[name] = Node(name, value)
    self.adj_list[name] = {}

  def add_vertex(self, name_a, name_b, w=1, directed=False):
    if name_a not in self.adj_list.keys(): self.add_node(name_a)
    if name_b not in self.adj_list.keys(): self.add_node(name_b)
    self.adj_list[name_a][name_b] = w
    if not directed: self.adj_list[name_b][name_a] = w

  def get_nodes(self):
    return set(self.nodes.values())

  def get_node_by_name(self, name):
    return self.nodes[name]

  def get_neighbors_of(self, node_name):
    return set([self.get_node_by_name(neigh_name) for neigh_name in self.adj_list[node_name].keys()])
  
  def get_cost(self, node_a, node_b):
    return self.adj_list[node_a.name][node_b.name]