def create_clusters(qty_clients: int , qty_trucks: int, cap_trucks: int, qty_poblacion: int, n_elite: int, n_generations: int, clients, prob_de_mut: float = 0.1):
    population = []

    for i in range(qty_poblacion):
        inv = []

        for j in range(qty_clients):
            inv.append(random.randint(0, qty_trucks-1))
            
        population.append(inv)

    #print(population)
    for generation in range(n_generations):
        population_fitness = [fitness(solution, qty_trucks, clients, cap_trucks) for solution in population]
        #print(population_fitness)

        parents = []
        for i in range(qty_poblacion):
            selection = random.sample(range(qty_poblacion), 2)
            #print(selection)

            if population_fitness[selection[0]] > population_fitness[selection[1]]:
                parents.append(population[selection[0]])
            else:
                parents.append(population[selection[1]])

            #print(parents)

        new_population = []
        for i in range(qty_poblacion):
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)

            if random.random() < prob_de_mut:
                i, j = random.sample(range(len(population)), 2)
                child[i], child[j] = child[j], child[i]

            new_population.append(child)

        new_fitness = [fitness(solution, qty_trucks, clients, cap_trucks) for solution in new_population]
        #print(new_fitness)

        population = list(zip(population, population_fitness))
        population = sorted(population, key = lambda x: x[1])
        population = [x[0] for x in population[:n_elite]]
        population_fitness = [fitness(solution, qty_trucks, clients, cap_trucks) for solution in population]

        combined_population = list(zip(population, population_fitness)) + list(zip(new_population, new_fitness))
        sorted_population = sorted(combined_population, key = lambda x: x[1])
        population = [x[0] for x in sorted_population[:qty_poblacion]]

    best_solution = population[0]
    for solution in population[1:]:
        if fitness(solution, qty_trucks, clients, cap_trucks) < fitness(best_solution, qty_trucks, clients, cap_trucks):
            best_solution = solution

    return best_solution


def crossover(parent1, parent2):
    op = random.randint(1, len(parent1) - 1)

    child = parent1[:op] + parent2[op:]
    #child2 = parent2[:op] + parent1[op:]

    return child#1, child2


def fitness(solution, qty_trucks, clients, cap_trucks):
    #print(solution)
    truck_clusters = []
    fitness = 0

    for cluster_id in range(qty_trucks):
        client_ids = find_indices(solution, cluster_id)

        truck_cluster = []

        for client_id in client_ids:
            truck_cluster.append(clients[client_id])
        
        truck_clusters.append(truck_cluster)

    for cluster in truck_clusters:
        total_cap = 0

        for client in cluster:
            total_cap += client.product

        if total_cap > cap_trucks:
            return inf
        
    fitness = distance(truck_clusters)

    return fitness


def distance(truck_clusters):
    distances = 0

    #print(truck_clusters)
    for truck_cluster in truck_clusters:
        for client in truck_cluster:
            for other_client in truck_cluster:
                
                if client == other_client:
                    continue

                distances += geoGraph.calculate_euclidian_distance(client.node.name, other_client.node.name)

        #print(len(truck_cluster))
        distances /= len(truck_cluster)*2

    return distances