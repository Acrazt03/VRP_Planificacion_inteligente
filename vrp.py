import geographs
import random
import math

geoGraph = geographs.GeoGraph()

class Client():
    def __init__(self, coords: tuple=None, time_window: tuple=None, product: float=10):

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

def create_nodes(Depot_coord: tuple, qty_clients: int, cap_trucks: int):
    
    Depot_node = geoGraph.get_nearest_geoNode(*Depot_coord)

    clients = []

    for i in range(qty_clients):
        client = Client()
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

def create_routes(depot_node: geographs.GeoNode, clients: list, truck_clusters: list, conn_radius: float):
    pass