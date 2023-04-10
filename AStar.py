from geographs import Graph, GeoNode, calculate_distance_coords
import heapq

class PriorityQueue():
  def __init__(self, data=[]):
    self.data = []
  
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

def heuristic_func(current_node: GeoNode, goal_node: GeoNode):
    distance =  calculate_distance_coords(current_node.lat, current_node.lon, goal_node.lat, goal_node.lon)#math.sqrt((current_node.lat - goal_node.lat)**2 + (current_node.lon - goal_node.lon)**2 )
    is_primary = 0 if not current_node.is_primary else 1
    n_lanes = current_node.n_lanes
    return distance*5 - is_primary*0.5 - n_lanes*0.5

def a_star_solver(graph: Graph, initial_node: GeoNode, goal_node: GeoNode):
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
            nodes_in_frontier = [node[1] for node in frontier.data]
            
            #print('Current Node: ', current_node)
            #print('is in cost: ', current_node in cost_of_path)
            #print('Condition 1: ', neighbor not in nodes_in_frontier and neighbor not in visited)
            #print('Condition 2: ', neighbor in nodes_in_frontier)

            neighbor_cost = cost_of_path[current_node] + graph.get_cost(current_node, neighbor)
            #if it is not in the frontier and has not been visited add it to the frontier with its value
            if(neighbor not in nodes_in_frontier and neighbor not in visited):
                #Calculate the heuristic cost for this node and add it to the PriorityQueue
                neighbor_node_heuristic_cost = heuristic_func(neighbor, goal_node)
                #print('Adding: ', neighbor)
                frontier.put((neighbor_cost + neighbor_node_heuristic_cost, neighbor))
                parents[neighbor] = current_node
                cost_of_path[neighbor] = neighbor_cost
            #elif it is in the frontier but you found a lower value, replace it in the frontier
            #elif neighbor in nodes_in_frontier:
            #    if frontier.putReplace((neighbor_cost, neighbor)):
            #        parents[neighbor] = current_node
            #        cost_of_path[neighbor] = neighbor_cost

    return False, visited, parents, cost_of_path#[goal_node]