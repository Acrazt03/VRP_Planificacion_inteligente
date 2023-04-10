import numpy as np

class Node:
  def __init__(self, name, value={}):
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
        
    self.node_to_index = {}
    self.index_to_node = {}


  def add_node(self, name, value={}):
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

  def get_adj_matrix(self, depot_node):
    self.node_to_index = {}
    self.index_to_node = {}

    depot_index = 0
    i = depot_index + 1

    for node in self.get_nodes():
      if node.name == depot_node.name:
        self.node_to_index[depot_node.name] = depot_index
        self.index_to_node[depot_index] = depot_node.name
      else:
        self.node_to_index[node.name] = i
        self.index_to_node[i] = node.name
        i += 1
    
    qty_nodes = len(self.get_nodes())
    adj_matrix = np.matrix(np.ones((qty_nodes,qty_nodes)) * np.inf)

    for node in self.get_nodes():
      node_idx = self.node_to_index[node.name]

      for neigh in self.get_neighbors_of(node.name):
        neigh_idx = self.node_to_index[neigh.name]

        adj_matrix[node_idx,neigh_idx] = self.get_cost(node, neigh)
      
    return adj_matrix.tolist()


  def add_node_and_connect(self, node_a, node_b, distance):
    if node_a.name not in self.nodes:
      self.nodes[node_a.name] = node_a

    if node_a.name not in self.adj_list:
      self.adj_list[node_a.name] = {}
    
    self.adj_list[node_a.name][node_b.name] = distance