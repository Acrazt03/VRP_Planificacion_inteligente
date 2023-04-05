import vrp

Depot_coord = (18.497205, -69.895533)
qty_clients = 10
cap_trucks = 100

Depot_node, clients, qty_trucks = vrp.create_nodes(Depot_coord, qty_clients, cap_trucks)

print(Depot_node)

for client in clients:
    print(client)

print(qty_trucks)