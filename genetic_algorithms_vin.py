import numpy as np
import random
import copy

inf = float('inf')
def create_population(population_num, cities_list, initial_city):
  cities = copy.copy(cities_list)
  cities.remove(initial_city)
  
  solutions = []
  for new_solution in range(population_num):
    solution = copy.copy(cities)
        
    random.shuffle(solution)
    solution.insert(0, initial_city)

    solutions.append(solution)

  return solutions


def calc_distances_paths(graph, initial_city, solutions):  
  distances = []

  for solution in solutions:
    distance = 0

    if len(solution) != len(set(solution)):
        distance = float('inf')
        distances.append(distance)
        continue

    for city_index in range(len(solution)-1):
      distance += graph[solution[city_index]][solution[city_index+1]]
    
    distance += graph[solution[-1]][initial_city]

    distances.append(distance)

  return distances


def calc_fitness(distances):
  fitnesess = np.exp2(-np.array(distances))*100
  
  return fitnesess


def crossover_solutions(solutions, population_num):
  crossovered_solutions = []

  #Keep the best alive for the next gen
  for solution in solutions:
    crossovered_solutions.append(solution)

  for new_solution in range(population_num-len(solutions)):
    crossover_point = random.randint(0, len(solutions[0]))
    
    parents = copy.deepcopy(random.sample(solutions, 2))

    cromosomeA = parents[0][:crossover_point]
    cromosomeB = parents[1][crossover_point:]

    solution = cromosomeA + cromosomeB

    crossovered_solutions.append(solution)

  return crossovered_solutions


def should_mutate(mutation_prob):
    return random.random() < mutation_prob


def mutate_solutions(solutions, mutation_prob):
  mutated_solutions = copy.deepcopy(solutions)

  for solution in mutated_solutions:
    if(should_mutate(mutation_prob)):

      #Swap two cities
      mutation_pointA, mutation_pointB = random.sample(range(1,len(solution)), 2)

      temp = copy.copy(solution[mutation_pointA])
      solution[mutation_pointA] = solution[mutation_pointB]
      solution[mutation_pointB] = temp
  
  return mutated_solutions


def sort_solutions_by_distance(gen_solutions, distances):
  sorted_lists = sorted(zip(gen_solutions, distances))
  return sorted_lists