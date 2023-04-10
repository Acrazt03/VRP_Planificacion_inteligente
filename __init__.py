import geographs
import random
import folium
import vrp

Depot_coord = (18.497205, -69.895533)
qty_clients = 300
cap_trucks = 100

print("Loading data... ")
geoGraph = geographs.GeoGraph()
print("Data loaded! ")

Depot_node, clients, qty_trucks = vrp.create_nodes(geoGraph, Depot_coord, qty_clients, cap_trucks)

print("Depot node: ", Depot_node)
#for client in clients:
#    print(client)
print("qty of trucks: ", qty_trucks)

qty_poblacion = 100
n_elite = 6
n_generations = 3
prob_de_mut = 0.1

solution = vrp.create_clusters(qty_clients, qty_trucks, qty_poblacion, n_elite, n_generations, prob_de_mut)
print("solution: ", solution)

conn_radius = 1
routes = vrp.create_routes(geoGraph, Depot_node, clients, qty_trucks, solution, conn_radius)

print("routes: ", routes)

for graph in routes:
    print(graph.get_nodes())

random_graph = routes[0]
for route in routes:
    nodes = random_graph.get_nodes()

    if len(nodes)==0:
        continue
    else:
        nodes = random.sample(random_graph.get_nodes(), k=2)
        break

print(nodes)

initial_node = nodes[0]
goal_node = nodes[1]

initial_marker = [initial_node.lat, initial_node.lon]
goal_marker = [goal_node.lat, goal_node.lon]

map = folium.Map(location=initial_marker, zoom_start=17)
folium.Marker(initial_marker).add_to(map)
folium.Marker(goal_marker).add_to(map)

path = initial_node.value

points = []
for node in path:
    point = [node.lat, node.lon]
    points.append(point)

folium.PolyLine(points, weight=5, opacity=1).add_to(map)
map.save("index.html")