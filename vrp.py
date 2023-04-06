import geographs
import random
import math

from graphs import Graph, Node

from AStar import a_star_solver

from routegraphs import RouteNode

class Client():
    def __init__(self, geoGraph, coords: tuple=None, time_window: tuple=None, product: float=10):

        if not coords:
            #Random
            self.node = geoGraph.get_random_node()
            self.coords = (self.node.lat, self.node.lon)
        
        if not time_window:
            start = random.randint(0, 24)
            self.time_window = (start, start+1)

        self.product = product

    def __str__(self) -> str:
        return f"Client {self.node.id} with time window: {self.time_window}, product: {self.product}, coords: {self.coords}"

def create_nodes(geoGraph, Depot_coord: tuple, qty_clients: int, cap_trucks: int):
    
    Depot_node = geoGraph.get_nearest_geoNode(*Depot_coord)

    clients = []

    for i in range(qty_clients):
        client = Client(geoGraph)
        clients.append(client)
    
    max_product_qty = 0

    for client in clients:
        max_product_qty += client.product

    qty_trucks = math.ceil(max_product_qty/cap_trucks)

    return Depot_node, clients, qty_trucks

def create_clusters(qty_clients: int , qty_trucks: int, qty_poblacion: int, n_elite: int, n_generations: int, prob_de_mut: float = 0.1):
    
    best_solution = []

    for i in range(qty_clients):
        best_solution.append(random.randint(0, qty_trucks-1))
    
    return best_solution

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

def reconstruct_path(geoGraph,start_node, goal_node, parent_node):
  path = [goal_node]

  current_parent = parent_node[goal_node]
  path.append(current_parent)

  while current_parent:

    next_parent = parent_node[current_parent]
    path.append(next_parent)

    if next_parent == start_node:
      break
    
    current_parent = next_parent
  
  path.reverse()

  cost = 0

  for i in range(len(path)-1):
    cost += geoGraph.get_cost(path[i], path[i+1])

  return path, cost

def create_routes(geoGraph,depot_node: geographs.GeoNode, clients: list, qty_trucks: int, clusters: list, conn_radius: float):

    #geoGraph = geographs.GeoGraph()
                    
    #truck_clusters = [0,1,2,0,0,1,1,2,2,0]
    #qty_trucks = 3

    truck_clusters = []

    for cluster_id in range(qty_trucks):
        client_ids = find_indices(clusters, cluster_id)

        truck_cluster = []

        for client_id in client_ids:
            truck_cluster.append(clients[client_id])
        
        truck_clusters.append(truck_cluster)

    #print("Truck Clusters: ", truck_clusters)

    graphs = []

    i = 1
    print(f"Truck {i}/{qty_trucks}")

    for truck_cluster in truck_clusters:
        graph = Graph()
        j = 1
        print(f"    Client: {j}/{len(truck_cluster)}")

        for client in truck_cluster:
            for other_client in truck_cluster:
            
                if client == other_client:
                    continue
            
                if geoGraph.calculate_euclidian_distance(client.node.name, other_client.node.name) <= conn_radius:
                    
                    print('     A Star')
                    SUCCESS, visited, parent_node, _ = a_star_solver(geoGraph, client.node, other_client.node)
                    #print('Success: ', SUCCESS)
                    #print('Visited: ', [node.name for node in visited])

                    if not SUCCESS:
                        continue

                    print('     Path reconstruct')
                    route, distance = reconstruct_path(geoGraph,client.node, other_client.node, parent_node)
                    #print(f'Distance: {distance:.2f} km')

                    #graph.add_node(name=client.node.name, value=route)
                    #graph.nodes[client.node.name].node = client.node
                    
                    client.node.value = route

                    graph.nodes[client.node.name] = client.node
                    graph.adj_list[client.node.name] = {}
                    
                    graph.add_vertex(client.node.name, other_client.node.name, w=distance, directed=True)
                
            print(f"    Client: {j}/{len(truck_cluster)}")
            j += 1

        print(f"Truck {i}/{qty_trucks}")

        i += 1
        graphs.append(graph)
    
    return graphs