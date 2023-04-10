import numpy as np
import random
import copy

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

def main():
  inf = float('inf')

  graph = [[inf, 3, 1, 2, 1],
          [3, inf, 1, 1, inf],
          [1, 1, inf, inf, 4],
          [2, 1, inf, inf, 1],
          [1, inf, 4, 1, inf]]

  #Params
  num_gen = 100
  population_num = 10
  solutions_to_choose = 3
  mutation_prob = 0.5

  cities = list(range(0,len(graph)))

  initial_city = 0

  #initial population
  solutions = create_population(population_num, cities, initial_city)
  best_solutions_by_gen = []

  #For each generation
  for gen in range(num_gen):
    #Calculate the total distance of each solution
    distances = calc_distances_paths(graph, initial_city, solutions)
    #print("distances: ", distances)
    
    #Calculate the fitness for each solution
    fitnesess = calc_fitness(distances)
    #print("fitnesess: ", fitnesess)

    #Choose k solutions randomly based on their fitnesess
    choosen_solutions = random.choices(solutions, weights=fitnesess, k=solutions_to_choose)
    #print("choosen solutions", choosen_solutions)

    #Save the best k solutions of this generation
    best_solutions_by_gen.append(choosen_solutions)

    #Use best solutions to create a new generation by croosover and mutation (based in mutation_prob)
    crossovered_solutions = crossover_solutions(choosen_solutions, population_num)
    #print("Crossovered_solutions: ", crossovered_solutions)
    solutions = mutate_solutions(crossovered_solutions, mutation_prob)
    #print("Mutated_solutions: ", solutions)

  best_solution_by_gen = []

  for gen_solutions in best_solutions_by_gen:
    distances = calc_distances_paths(graph, initial_city, gen_solutions)
    best_solution_of_gen = sort_solutions_by_distance(gen_solutions, distances)[-1]
    best_solution_by_gen.append(best_solution_of_gen)

  final_answer = sorted(best_solution_by_gen,key=lambda x: x[1])[0]

  print("Answer: ", final_answer)
  print(solutions)


if __name__ == '__main__':
  main()