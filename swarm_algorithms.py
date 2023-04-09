from memory_profiler import profile
import numpy as np

#@profile
def floyd_warshall(grafo):
    #inicializa la la ruta hacia la misma ciudad a 0
    for i in range(len(grafo)):
        grafo[i][i] = 0

    # Crea las rutas faltantes entre el grafo
    for k in range(len(grafo)):
        for i in range(len(grafo)):
            for j in range(len(grafo)):
                aux = grafo[i][k] + grafo[k][j]

                if grafo[i][j] > aux:
                    grafo[i][j] = aux

    return grafo

# Algoritmo de la colonia de hormigas (ACO)
class ACO:
    #@profile
    def __init__(self, cities, ants = 30, generations = 100, ev_rate = 0.5, alpha = 1, beta = 2, start_city = None):
        self.cities = np.array(floyd_warshall(cities))
        self.ants = ants
        self.generations = generations
        self.ev_rate = ev_rate
        self.alpha = alpha
        self.beta = beta

        # Inicializa la ciudad de ser nula
        if start_city == None:
            self.start_city = np.random.randint(len(cities))
        else:
            self.start_city = start_city
                
        self.pheromones = np.ones(self.cities.shape)

    #@profile
    def solve(self):
        best_solution = None
        best_score = float('inf')

        for iteration in range(self.generations):
            for ant in range(self.ants):

            	# Ciudad de inicio para el vendedor
                current_city = self.start_city
                visited_cities = [current_city]

                while len(visited_cities) < len(self.cities):
                    next_city = self.transition(current_city, visited_cities, self.pheromones, self.cities, self.alpha, self.beta)
                    visited_cities.append(next_city)
                    current_city = next_city

                visited_cities.append(self.start_city)
                score = self.solution(visited_cities, self.cities)
                
                if score < best_score:
                    best_solution = visited_cities
                    best_score = score

                for i in range(len(visited_cities)-1):
                    c1 = visited_cities[i]
                    c2 = visited_cities[i+1]
                    self.pheromones[c1, c2] = (1 - self.ev_rate) * self.pheromones[c1, c2] + self.ev_rate / score
                    self.pheromones[c2, c1] = (1 - self.ev_rate) * self.pheromones[c2, c1] + self.ev_rate

                    return best_solution, best_score

    #@profile
    def transition(self, current_city, visited_cities, pheromones, cities, alpha, beta):
        unvisited_cities = np.delete(np.arange(len(cities)), visited_cities)
        prob = np.zeros(len(unvisited_cities))

        for i, city in enumerate(unvisited_cities):
            prob[i] = (pheromones[current_city, city] ** alpha) * ((1.0 / cities[current_city, city]) ** beta)

        prob /= prob.sum()
        next_city = np.random.choice(unvisited_cities, p=prob)
        
        return next_city

    #@profile
    def solution(self, solution, cities):
        return sum(cities[solution[i], solution[i+1]] for i in range(len(solution)-1)) + cities[solution[-1], self.start_city]


# Algoritmo de la colonia de abejas (ABC)


# Algoritmo de la optimización de enjambre de partículas (PSO)


# Algoritmo de la optimización de enjambre de luciérnagas (FIREFLY ALGORITHM)


# Algoritmo de la optimización de enjambre de efímeras (MAYFLY ALGORITHM)
class MayflyAlgorithm:
    def __init__(self, n_cities, n_mayfly, generations, weight, c1, c2):
        self.n_cities = n_cities
        self.n_mayfly = n_mayfly
        self.generations = generations
        self.weight = weight
        self.c1 = c1
        self.c2 = c2
        self.positions = None
        self.velocities = None
        self.personal_bests = None
        self.global_best_position = None
        self.global_best_fitness = float('inf')

    def calculate_distance_matrix(self, positions):
        distance_matrix = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(i, self.n_cities):
                distance_matrix[i, j] = distance_matrix[j, i] = np.linalg.norm(positions[i] - positions[j])
        return distance_matrix

    def calculate_fitness(self, positions, distance_matrix):
        fitness = 0
        for i in range(self.n_mayfly):
            path = np.argsort(positions[i])
            distance = 0
            for j in range(self.n_cities - 1):
                distance += distance_matrix[path[j], path[j+1]]
            distance += distance_matrix[path[-1], path[0]]
            fitness += distance
        return fitness

    def update_velocities(self, velocities, positions, personal_bests, global_best_position):
        r1 = np.random.rand(self.n_mayfly, self.n_cities, 2)
        r2 = np.random.rand(self.n_mayfly, self.n_cities, 2)
        cognitive = self.c1 * r1 * (personal_bests - positions)
        social = self.c2 * r2 * (global_best_position - positions)
        new_velocities = self.weight * velocities + cognitive + social
        return new_velocities

    def update_positions(self, positions, velocities):
        new_positions = positions + velocities
        return new_positions

    def run(self):
        self.positions = np.random.rand(self.n_mayfly, self.n_cities, 2)
        self.velocities = np.zeros((self.n_mayfly, self.n_cities, 2))
        self.personal_bests = self.positions.copy()

        distance_matrix = self.calculate_distance_matrix(self.positions)
        fitness = self.calculate_fitness(self.positions, distance_matrix)

        self.personal_bests = self.positions.copy()
        if fitness < self.global_best_fitness:
            self.global_best_position = self.positions.copy()
            self.global_best_fitness = fitness

        for i in range(self.generations):
            self.velocities = self.update_velocities(self.velocities, self.positions, self.personal_bests, self.global_best_position)
            self.positions = np.clip(self.positions, 0, 1)

        distance_matrix = self.calculate_distance_matrix(self.positions)
        fitness = self.calculate_fitness(self.positions, distance_matrix)

        better_personal_bests = fitness < self.calculate_fitness(self.personal_bests, distance_matrix)
        self.personal_bests[better_personal_bests] = self.positions[better_personal_bests]
        if fitness < self.global_best_fitness:
            self.global_best_position = self.positions.copy()
            self.global_best_fitness = fitness

        return self.global_best_position, self.global_best_fitness
