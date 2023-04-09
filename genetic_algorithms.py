from memory_profiler import profile
import numpy as np
import random

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

# Algoritmos genéticos
class GeneticAlgorithm:
    #@profile
    def __init__(self, cities, start_city = None,  population_size = 5, num_generations = 2000):
        self.cities = floyd_warshall(cities)
        self.population_size = population_size
        self.num_generations = num_generations

        # Asigna la posicion inicial
        if start_city == None:
            self.start_city = np.random.randint(len(cities))
        else:
            self.start_city = start_city
    
    #@profile
    def total_distance(self, solution):
        distance = 0
        for i in range(len(solution)-1):
            distance += self.cities[solution[i]][solution[i+1]]
            distance += self.cities[solution[-1]][solution[0]]

        return distance

    #@profile
    def pmx(self, parent1, parent2):
        n = (len(parent1) | len(parent2))//2

        child1 = parent1[:n] + parent2[n:]
        child2 = parent2[:n] + parent1[n:]

        secc1 = parent1[:n]
        secc2 = parent2[:n]

        map1 = dict(zip(secc1, secc2))
        map2 = dict(zip(secc2, secc1))

        new_child1 = secc1 + [x if x not in secc1 else 'x' for x in child1[n:]]
        new_child2 = secc2 + [x if x not in secc2 else 'x' for x in child2[n:]]

        for idx, i in enumerate(new_child1):
          if i == 'x':
            vmap = child1[idx]
            while vmap in new_child1:
              vmap = map1[vmap]

            new_child1[idx] = vmap

        for idx, i in enumerate(new_child2):
          if i == 'x':
            vmap = child2[idx]
            while vmap in new_child2:
              vmap = map2[vmap]

            new_child2[idx] = vmap

        return new_child1, new_child2

    #@profile
    def mutation(self, child):
        if random.random() < 0.05:
            i, j = random.sample(range(len(self.cities)), 2)
            child[i], child[j] = child[j], child[i]

        return child

    #@profile
    def solve(self):
        # Genera una población inicial de soluciones aleatorias
        population = []

        for i in range(self.population_size):
            solution = list(range(len(self.cities)))
            random.shuffle(solution)
            population.append(solution)

        #print(population)
        # Evoluciona la población durante un número determinado de generaciones
        for generation in range(self.num_generations):
            # Evalúa la aptitud de cada solución
            fitness = [self.total_distance(solution) for solution in population]

            # Selecciona los padres para la siguiente generación
            parents = []

            for i in range(self.population_size):
                # Selecciona dos padres al azar 
                selection = random.sample(range(self.population_size), 2)

                if fitness[selection[0]] > fitness[selection[1]]:
                    parents.append(population[selection[0]])
                else:
                    parents.append(population[selection[1]])

            # Crea una nueva generación a partir de los padres seleccionados
            new_population = []

            parent1, parent2 = random.sample(parents, 2)

            child1, child2 = self.pmx(parent1, parent2)

            child1 = self.mutation(child1)
            child2 = self.mutation(child2)                

            new_population.append(child1)
            new_population.append(child2)

            # Evalúa la aptitud de la nueva generación
            new_fitness = [self.total_distance(solution) for solution in new_population]
            combined_population = list(zip(population, fitness)) + list(zip(new_population, new_fitness))
            sorted_population = sorted(combined_population, key = lambda x: x[1])

            population_aux = []
            for solution in sorted_population:
                if solution[0][-1] == self.start_city:
                    population_aux.append(solution)

            population_aux = sorted(population_aux, key = lambda x: x[1])
            new_combined_population = population_aux + sorted_population
            population = [x[0] for x in new_combined_population[:self.population_size]]
            
            #print("1:",population_aux,"\n") 
            #print("2:",sorted_population,"\n")
            #print("3:",new_combined_population,"\n")
            #print("4:",population,"\n\n\n")
            #print(self.total_distance(population[0]))

        # Devuelve la mejor solución encontrada
        best_solution = population[0]
        for solution in population[1:]:
            if solution[-1] == self.start_city:
                if self.total_distance(solution) < self.total_distance(best_solution) and solution[-1] == self.start_city:
                    best_solution = solution

        best_solution.insert(0, self.start_city)
        return best_solution, self.total_distance(best_solution)