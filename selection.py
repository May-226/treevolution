from __future__ import division
from random import choice, randint, uniform


def ElitistSelection(gevolver, percentage = 0.25):
    gevolver.population.sort(key=lambda t: gevolver.fitness(t),reverse=True)
    gevolver.population = gevolver.population[:-int(percentage*len(gevolver.population))]
    for i in range(int(percentage*len(gevolver.population))):
        randomCrossoverOperator = gevolver.randomCrossoverOperator()
        gevolver.population.append(randomCrossoverOperator
                            (gevolver.randomIndividual(), gevolver.randomIndividual()))
 
def RouletteWheelSelection(gevolver, f):
    pointer = 0
    for individual in gevolver.population:
        if pointer < f and pointer + gevolver.fitness(individual) > f:
            return individual
        pointer += gevolver.fitness(individual)
           
def StochasticUniversalSampling(gevolver, surviving=5):
    gevolver.population.sort(key=lambda t: gevolver.fitness(t),reverse=True)
    
    cumFit = sum([gevolver.fitness(individual) for individual in gevolver.population])
    start = uniform(0, cumFit/surviving)
    pointers =  [start + i*(cumFit/surviving) for i in range(0, surviving)]
    newpopulation = [RouletteWheelSelection(gevolver,i) for i in pointers]
    gevolver.population = newpopulation
    for i in range(gevolver.size-surviving):
        randomMutationOperator = gevolver.randomMutationOperator()
        gevolver.population.append(randomMutationOperator(gevolver,gevolver.randomIndividual()))
    
def TournamentSelection(gevolver, tournament_size = 2, surviving = 1):
    competing_individuals = []
    for i in range(tournament_size):
        competing_individuals[i]=choice(range(gevolver.population))
    competing_individuals.sort(key=lambda ind: gevolver.fitness(gevolver.population[ind]))
    competing_individuals = competing_individuals[surviving:]
    
    for ind in competing_individuals:
        gevolver.population[ind] = gevolver.randomCrossoverOperator()(gevolver.randomIndividual(), gevolver.randomIndividual())
    