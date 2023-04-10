from routegraphs import RouteNode
from AStar import a_star_solver
from graphs import Graph, Node
import geographs
import random
import math
import numpy as np

class Client():
    def __init__(self, geoGraph, coords: tuple=None, time_window: tuple=None, product: int=10):#random.randint(0, 10)):

        if not coords:
            #Random
            self.node = geoGraph.get_random_node()
            self.coords = (self.node.lat, self.node.lon)
            self.name = self.node.name
        
        if not time_window:
            start = random.randint(0, 24)
            self.time_window = (start, start+1)

        self.product = product

    def __str__(self) -> str:
        return f"Client {self.node.id} with time window: {self.time_window}, product: {self.product}, coords: {self.coords}"

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

class create_clusters:
    def __init__(self, geoGraph, qty_clients: int , qty_trucks: int, cap_trucks: int, qty_poblacion: int, n_elite: int, n_generations: int, clients, prob_de_mut: float = 0.1):
        self.qty_poblacion = qty_poblacion
        self.n_generations = n_generations
        self.prob_de_mut = prob_de_mut
        self.qty_clients = qty_clients
        self.qty_trucks = qty_trucks
        self.cap_trucks = cap_trucks
        self.geoGraph = geoGraph
        self.n_elite = n_elite
        self.clients = clients 

    def create_clusters(self):
        population = []

        for i in range(self.qty_poblacion):
            inv = []

            for j in range(self.qty_clients):
                inv.append(random.randint(0, self.qty_trucks-1))
                
            population.append(inv)

        for _ in range(self.n_generations):
            population_fitness = [self.fitness(solution) for solution in population]

            #Selection
            population_fitness_pair = list(zip(population, population_fitness))
            n_elite_pairs = sorted(population_fitness_pair, key = lambda x: x[1])[:self.n_elite]
            n_elite_individuals = [x[0] for x in n_elite_pairs]

            qty_individuals_to_create = self.qty_poblacion - self.n_elite

            #Creation
            population = []
            for i in range(qty_individuals_to_create//2):
                parent_1, parent_2 = random.sample(n_elite_individuals, 2)

                child1, child2 = self.crossover(parent_1, parent_2)
                population.append(child1)
                population.append(child2)

            #Mutation
            for individual in population:
                if random.random() < self.prob_de_mut:
                    i, j = random.sample(range(len(individual)), 2)
                    individual[i], individual[j] = individual[j], individual[i]

            population = n_elite_individuals + population

        population_fitness = [self.fitness(solution) for solution in population]
        population_fitness_pair = list(zip(population, population_fitness))
        sorted_population = sorted(population_fitness_pair, key = lambda x: x[1])
        solutions = [x[0] for x in sorted_population]
        best_solution = solutions[0]

        return best_solution

    def crossover(self, parent1, parent2):
        op = random.randint(1, len(parent1) - 1)

        child1 = parent1[:op] + parent2[op:]
        child2 = parent2[:op] + parent1[op:]

        return child1, child2

    def fitness(self, solution):
        truck_clusters = []
        fitness = 0

        for cluster_id in range(self.qty_trucks):
            client_ids = find_indices(solution, cluster_id)

            truck_cluster = []
            for client_id in client_ids:
                truck_cluster.append(self.clients[client_id])
            
            truck_clusters.append(truck_cluster)

        for cluster in truck_clusters:
            total_cap = 0

            for client in cluster:
                total_cap += client.product

            if total_cap > self.cap_trucks:
                return float('inf')
            
        fitness = self.distance(truck_clusters)
        return fitness

    def distance(self, truck_clusters):
        distances = 0

        for truck_cluster in truck_clusters:
            for client in truck_cluster:
                for other_client in truck_cluster:
                    
                    if client == other_client:
                        continue

                    distances += self.geoGraph.calculate_euclidian_distance(client.node.name, other_client.node.name)

            #distances /= len(truck_cluster)

        return distances

def create_nodes(geoGraph, Depot_coord: tuple, qty_clients: int, cap_trucks: int):
    
    Depot_node = geoGraph.get_nearest_geoNode(*Depot_coord)

    clients = []

    for i in range(qty_clients):
        clients.append(Client(geoGraph))
    
    max_product_qty = 0

    for client in clients:
        max_product_qty += client.product

    qty_trucks = math.ceil(max_product_qty/cap_trucks)

    return Depot_node, clients, qty_trucks

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
    if not path[i]:
        continue
        raise Exception('El primer path dio problemas')
    elif not path[i+1]:
        continue
        raise Exception('El segundo path dio problemas')
    
    cost += geoGraph.get_cost(path[i], path[i+1])

  return path, cost

def get_n_nearest_nodes(node_a, other_nodes, n_nearest_nodes):
      nodes = list(other_nodes)

      sorted_nodes = sorted(nodes, key = lambda node_b: geographs.calculate_distance_coords(node_a.lat, node_a.lon, node_b.lat, node_b.lon) if node_a.name != node_b.name else float('inf'))

      if len(sorted_nodes) >= n_nearest_nodes:
         return sorted_nodes[:n_nearest_nodes]
      else:
         return sorted_nodes

def create_routes(geoGraph,depot_node: geographs.GeoNode, clients: list, qty_trucks: int, clusters: list, n_nearest_nodes: int):

    truck_clusters = []

    for cluster_id in range(qty_trucks):
        client_ids = find_indices(clusters, cluster_id)

        truck_cluster = []

        for client_id in client_ids:
            truck_cluster.append(clients[client_id])
        
        truck_clusters.append(truck_cluster)

    #print("Truck Clusters: ", truck_clusters)

    graphs = []
    paths = []

    i = 1

    for truck_cluster in truck_clusters:
        graph = Graph()
        route_paths = {}
        print(f"Truck {i}/{qty_trucks}")
        #print(f"Len del client cluster: {len(truck_cluster)}")

        for client in truck_cluster:
            path = {}

            other_nodes = [other_truck_client.node for other_truck_client in truck_cluster]
            nearest_nodes = get_n_nearest_nodes(client.node, other_nodes, n_nearest_nodes)

            nearest_nodes.append(depot_node)

            #print(f"Nearest nodes for client {client.node.name}: {[near_node.name for near_node in nearest_nodes]}")

            for other_client in nearest_nodes:
                route = connect_nodes(geoGraph, graph, client.node, other_client)
                path[other_client.name] = route

            route_paths[client.node.name] = path
        
        other_nodes = [other_truck_client.node for other_truck_client in truck_cluster]

        for other_client in other_nodes:
            route = connect_nodes(geoGraph, graph, depot_node, other_client)
            path[other_client.name] = route

        route_paths[depot_node.name] = path

        i += 1        
        paths.append(route_paths)
        graphs.append(graph)
    
    return graphs, paths

def connect_nodes( geoGraph, graph, initial_node, goal_node):

    #print(f"Connecting {initial_node.name} and {goal_node.name}")
    SUCCESS, visited, parent_node, _ = a_star_solver(geoGraph, initial_node, goal_node)

    if not SUCCESS:
        #raise Exception(f"Sorry, A Star Didn't work \n{visited}\n{parent_node}\n{_}")
        print(f"A Star couldn't find a path between {initial_node.name} and {goal_node.name}")
        return []

    route, distance = reconstruct_path(geoGraph,initial_node, goal_node, parent_node)

    graph.add_node_and_connect(initial_node, goal_node, distance)
    return route