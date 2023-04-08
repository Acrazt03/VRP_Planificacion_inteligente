import copy
import random
import numpy

inf = float('inf')

class Ant:
  
  def __init__(self, Original_graph, initial_city, params):

    self.inf = float('inf')
    #Variable that saves the distance the ant has walked
    self.path_distance = 0
    #Set the starting node (current_city is a list of distances to other nodes)
    self.graph = copy.deepcopy(Original_graph)
    self.current_city = copy.deepcopy(self.graph[initial_city])
    
    #Set the initial node as visited, so the ant doesn't move in a loop on it
    self.visited_cities = []
    self.visited_cities.append(initial_city)
    self.initial_city = initial_city

    #Params
    self.desirability_exp = params[0]

    self.pheromone_Initial_Intensity = params[1]
    self.pheromone_Intensity = params[2]
    self.pheromone_exp = params[3]
    self.pheromone_evaporation_rate = params[4]
  
  def check_visited(self):
    #Set the distance to already visited cities to inf(so the ant doesn't move to those)
    for visited_city_index in range(len(self.visited_cities)):
      self.current_city[self.visited_cities[visited_city_index]] = self.inf
  
  def pow_list(self, list, power=1): 
    return [number**power for number in list]

  def calc_desirabilities(self,pheromones_traces):

    canMove = False

    for candidate_city in self.current_city:
      if(candidate_city != self.inf):
        canMove = True
    
    if(canMove):
    #Calculate the desirability to move to each child node
    #Using the equation which takes in cosideration the distance to the nodes and how many pheromones the path(vertex) currently has
      self.desirabilities = self.pow_list(self.current_city,-self.desirability_exp)*(pheromones_traces[self.graph.index(self.current_city)]**self.pheromone_exp)
    #print("Desirabilities: ", self.desirabilities)
    else:
      self.desirabilities = []

  def move(self):
    #Get a list (a range) with the indexes for all the child cities of the current cities
    #To use it as different options for random.choices
    distances_indexes = list(range(0,len(self.current_city)))

    #Check if all the child cities are already visited(distance = inf)
    if(len(self.desirabilities) > 0):
      #if not, the choose randomly the next city to go to (base on their respective desirabilities)
      self.next_city = random.choices(distances_indexes, weights=self.desirabilities, k=1)[0]
    else:
      #if there are no more cities left to visit, stop
      return

    if(self.current_city[self.next_city] == inf):
      print("Moved when it wasn't suposed to")
    
    #Acumulate the distance that the ant walks
    self.path_distance += self.current_city[self.next_city]

    #Set the current city to the next city that was choosen
    self.current_city_index = self.next_city
    self.current_city = self.graph[self.next_city]

    #Add the next city to the visited cities list
    self.visited_cities.append(self.next_city)
  
  def come_back(self, Original_graph):
    #Move the ant to the initial city and add the distance to the total path distance
    self.path_distance += Original_graph[self.current_city_index][self.initial_city]

  def leave_pheromones(self, pht):

    #Loop to go truh each visited city (-1 the last one, maybe should cahnge it later)
    for visited_city_index in range(len(self.visited_cities)-1):
      #Update the pheromones trace strenght of the path's vertex, proportionally to the total distance of the answered path by the ant
      pht[self.visited_cities[visited_city_index],self.visited_cities[visited_city_index+1]] += self.pheromone_Intensity*self.path_distance
    
    #print(self.visited_cities)
    
    return pht

class Colony:
  
  def __init__(self, Graph, ants_num, pheromones_traces, params):

    self.inf = 999999
    self.Ants = []

    self.answer = []
    self.current_distance = 999999

    self.graph = copy.deepcopy(Graph)
    self.pheromones_traces = pheromones_traces

    #Params
    self.desirability_exp = params[0]

    self.pheromone_Initial_Intensity = params[1]
    self.pheromone_Intensity = params[2]
    self.pheromone_exp = params[3]
    self.pheromone_evaporation_rate = params[4]

    self.ants_number = ants_num
    self.params = params

  def solve(self, Original_graph, initial_city, iterations=1):
    
    #Loop for each iteration
    for iteration in range(iterations):

      #Kill the remaining ants and create new one
      self.Ants.clear()
      for ant in range(self.ants_number):
        self.Ants.append(Ant(self.graph, initial_city, self.params))

      for city in range(len(self.graph)-1):
        #Evaporate the pheromones
        self.pheromones_traces -= self.pheromones_traces*self.pheromone_evaporation_rate
        
        #Tell each ant to:
        #Look if it can move to the next city
        #Calc a desiarability for each of those cities
        #Move to it
        for ant in self.Ants:
          ant.check_visited()
          ant.calc_desirabilities(self.pheromones_traces)
          ant.move()
      
      #loop to send the ants back to the initial city and update pheromones
      for ant in self.Ants:
        ant.come_back(Original_graph)
        self.pheromones_traces = ant.leave_pheromones(self.pheromones_traces)
        #print(ant.path_distance, self.current_distance)
        #Save the path with the shortest distance
        if(ant.path_distance < self.current_distance):
          self.answer = ant.visited_cities
          self.current_distance = ant.path_distance
    
    return self.answer