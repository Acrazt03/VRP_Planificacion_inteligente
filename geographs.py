from math import sin, cos, sqrt, atan2, radians
from graphs import Node, Graph
import osmium as osm
import random
import heapq

class GeoNode(Node):
    def __init__(self, id, x, y, lat, lon):
        self.id = id
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon
        self.available = True
        self.is_primary = False
        self.n_lanes = 0
        super().__init__(id)
    
    def __str__(self):
        return f"GeoNode {self.id} at pos {self.x, self.y}, coords {self.lat, self.lon}"
    

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.nodes = []
        self.ways = []
        self.node_highway_values = set()
        self.way_highway_values = set()
        self.way_highway_values_list = []

        #self.allowed_ways = set(['primary_link', 'tertiary', 'primary', 'path', 'secondary', 'trunk', 'corridor', 'pedestrian', 'service', 'raceway', 'construction', 'residential', 'steps', 'trunk_link', 'cycleway', 'tertiary_link', 'motorway', 'footway', None, 'living_street', 'motorway_link', 'secondary_link', 'unclassified', 'road', 'track'])
        #self.allowed_ways = set(['primary_link', 'tertiary', 'primary', 'secondary', 'trunk', 'service', 'raceway', 'construction', 'residential', 'trunk_link', 'tertiary_link', 'motorway', 'living_street', 'motorway_link', 'secondary_link', 'track'])
        #self.allowed_ways = set(['primary_link', 'primary', 'secondary', 'trunk', 'trunk_link', 'tertiary_link' 'secondary_link'])
        #self.allowed_ways = set(['primary_link', 'primary'])
        #self.allowed_ways = set(['primary', 'secondary', 'tertiary', 'trunk','primary_link', 'motorway', 'motorway_link'])
        #https://wiki.openstreetmap.org/wiki/Key:highway?uselang=en#Highway
        self.allowed_ways = set(['primary', 'secondary', 'tertiary', 'trunk','primary_link', 'motorway', 'motorway_link', 'residential'])


    def node(self, node):
        self.node_highway_values.add(node.tags.get('highway'))

        #if(node.tags.get('highway') == 'crossing'):
        self.nodes.append((node.id, node.location.x, node.location.y, node.location.lat, node.location.lon))


    def way(self, way):
        self.way_highway_values.add(way.tags.get('highway'))
        self.way_highway_values_list.append(way.tags.get('highway'))

        if(way.tags.get('highway') in self.allowed_ways):
            
            nodes = []

            for node in way.nodes:
                nodes.append(node)
            
            #is_closed = way.is_closed()
            directed = way.tags.get('oneway') != 'yes'
            is_primary = way.tags.get('highway') != 'residential'
            if way.tags.get('lanes'):
                n_lanes = int(way.tags.get('lanes'))
            else:
                n_lanes = 0
            self.ways.append((nodes, directed, is_primary, n_lanes))


#haversine
def calculate_distance_coords(lat1, lon1, lat2, lon2):
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


class GeoGraph(Graph):
    def __init__(self, osm_file_path='santo_domingo.osm', limit_coords=None):
        super().__init__()

        self.osmHandler = OSMHandler()
        self.osmHandler.apply_file(osm_file_path)

        #print('nodes highway: ', self.osmHandler.node_highway_values)
        #print('ways highway: ', self.osmHandler.way_highway_values)
        #print('Qty each way: ')

        #for value in self.osmHandler.way_highway_values:
        #    print(f'for {value} there are: {self.osmHandler.way_highway_values_list.count(value)}')

        #print('intersection: ', self.osmHandler.node_highway_values.intersection(self.osmHandler.way_highway_values))

        for node in self.osmHandler.nodes:
            self.add_geo_node(node[0], node[1], node[2], node[3], node[4])

        for way in self.osmHandler.ways:
            self.add_way(way[0], way[1], way[2], way[3])

        for node in self.get_nodes():
            if len(self.get_neighbors_of(node.name)) == 0:
                self.nodes[node.name].available = False
        
        #available_nodes = [node for node in self.get_nodes() if node.available]
        #print(f'Available nodes before condition: {len(available_nodes)}')

        if limit_coords:
          centroid_node = self.get_nearest_geoNode(*limit_coords)
          for node in self.get_nodes():
            if self.calculate_euclidian_distance(centroid_node.name, node.name) >= 4:
               self.nodes[node.name].available = False

        #available_nodes = [node for node in self.get_nodes() if node.available]
        #print(f'Available nodes after condition: {len(available_nodes)}')
        

    def add_geo_node(self, id, x, y, lat, lon):
        self.nodes[id] = GeoNode(id, x, y, lat, lon)
        self.adj_list[id] = {}


    def calculate_euclidian_distance(self, node_name_a, node_name_b):
        node_a: GeoNode = self.get_node_by_name(node_name_a)
        node_b: GeoNode = self.get_node_by_name(node_name_b)

        distance = calculate_distance_coords(node_a.lat, node_a.lon, node_b.lat, node_b.lon)#math.sqrt((node_a.lat - node_b.lat)**2 + (node_a.lon - node_b.lon)**2 )
        return distance


    def add_way(self, nodes, directed, is_primary, n_lanes):
        for i in range(len(nodes)-1):

            name_a = nodes[i].ref
            name_b = nodes[i+1].ref

            if is_primary:
                self.nodes[name_a].is_primary = is_primary
                self.nodes[name_b].is_primary = is_primary

            if n_lanes:
                self.nodes[name_a].n_lanes = n_lanes
                self.nodes[name_b].n_lanes = n_lanes

            distance = self.calculate_euclidian_distance(name_a, name_b)
            
            try:
                self.adj_list[name_a][name_b] = distance
                if directed: self.adj_list[name_b][name_a] = distance
            except KeyError:
                print('node not found')
    
    
    def get_nearest_geoNode(self, lat, lon):
        min_distance = 0.05

        for geoNode in self.get_nodes():
            if geoNode.available:
                distance = calculate_distance_coords(geoNode.lat, geoNode.lon, lat, lon)

                if distance < min_distance:
                    return geoNode
    

    def get_random_node(self):
      available_nodes = [node for node in self.get_nodes() if node.available]
      return self.select_random_node(available_nodes)
    

    def select_random_node(self, nodes):
      random_node = random.sample(nodes, 1)[0]
      
      if random_node.available:
        return random_node
      else:
        return self.select_random_node()


class PriorityQueue():
  def __init__(self, data=[]):
    self.data = data
  
  def put(self, value):
    heapq.heappush(self.data, value)

  def get(self):
    return heapq.heappop(self.data)

  def isEmpty(self):
    return len(self.data) == 0
  
  def view(self):
    return heapq.heapify(self.data)

  def putReplace(self, value):
    for data in self.data:
      if value[1] == data[1]:
        if value[0] < data[0]:
          self.data.remove(data)
          self.put(value)

          return True
        
    return False


def a_star_solver(graph: Graph, initial_node: GeoNode, goal_node: GeoNode, heuristic_func):
  frontier = PriorityQueue()
  frontier.put((0, initial_node))

  #Stores the order on which the nodes were visited
  visited = []
  
  #Stores the cost from the start node to the current node
  cost_of_path = {}
  cost_of_path[initial_node] = 0

  parents = {}
  parents[initial_node] = None

  while not frontier.isEmpty():
    value, current_node = frontier.get()

    visited.append(current_node)
    if current_node == goal_node:
      return True, visited, parents,cost_of_path#[goal_node]

    for neighbor in graph.get_neighbors_of(current_node.name):
      neighbor_cost = cost_of_path[current_node] + graph.get_cost(current_node, neighbor)
      nodes_in_frontier = [node[1] for node in frontier.data]

      #if it is not in the frontier and has not been visited add it to the frontier with its value
      if(neighbor not in nodes_in_frontier and neighbor not in visited):
        #Calculate the heuristic cost for this node and add it to the PriorityQueue
        neighbor_node_heuristic_cost = heuristic_func(neighbor, goal_node)
        frontier.put((neighbor_cost + neighbor_node_heuristic_cost, neighbor))
        parents[neighbor] = current_node
        cost_of_path[neighbor] = neighbor_cost

      #elif it is in the frontier but you found a lower value, replace it in the frontier
      elif neighbor in nodes_in_frontier:
        if frontier.putReplace((neighbor_cost, neighbor)):
          parents[neighbor] = current_node
          cost_of_path[neighbor] = neighbor_cost

  return False, visited, parents, cost_of_path#[goal_node]


def heuristic_function(current_node: GeoNode, goal_node: GeoNode):
    distance = calculate_distance_coords(current_node.lat, current_node.lon, goal_node.lat, goal_node.lon)#math.sqrt((current_node.lat - goal_node.lat)**2 + (current_node.lon - goal_node.lon)**2 )
    is_primary = 0 if not current_node.is_primary else 1
    n_lanes = current_node.n_lanes
    return distance*5 - is_primary*0.5 - n_lanes*0.5