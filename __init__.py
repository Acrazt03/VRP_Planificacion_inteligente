import vrp

Depot_coord = (18.497205, -69.895533)
qty_clients = 24
cap_trucks = 80

Depot_node, clients, qty_trucks = vrp.create_nodes(Depot_coord, qty_clients, cap_trucks)

print(Depot_node)

for client in clients:
    print(client)

print(qty_trucks)

qty_poblacion = 100
n_elite = 6
n_generations = 3
prob_de_mut = 0.1

solution = vrp.create_clusters(qty_clients, qty_trucks, qty_poblacion, n_elite, n_generations, prob_de_mut)

conn_radius = 0.5

print(vrp.create_routes(Depot_node, clients, qty_trucks, solution, conn_radius))

