import geographs
import random

geoGraph = geographs.GeoGraph()

class Client():
    def __init__(self, coords: tuple=None, time_window: tuple=None, product: float=1):

        if not coords:
            #Random
            self.node = geoGraph.get_random_node()
            self.coords = (self.node.lat, self.node.lon)
        
        if not time_window:
            start = random.randint(0, 24)
            self.time_window = (start, start+1)

        self.product = product

def create_nodes(Depot_coord: tuple, qty_clients: int, cap_trucks: int):
    
    Depot_node = geoGraph.get_nearest_geoNode(Depot_coord)

    clients = []

    for i in range(qty_clients):
        client = Client()
        clients.append(client)
    
    max_product_qty = 0

    for client in clients:
        max_product_qty += client.product

    qty_trucks = max_product_qty/cap_trucks

    return Depot_node, clients, qty_trucks