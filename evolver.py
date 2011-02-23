from crossover import SwitchCrossover
from mutation import changeSubTreeMutation
from selection import StochasticUniversalSampling
from growing import full,grow
from nodetype import *
from tree import *
import toolkit
from functools import partial


class evolver:
    def __init__(self, 
                 fitnessFunc = None, 
                 size = 10, mindepth = 3, maxdepth = 10, 
                 growing_methods = [full,grow],
                 crossover_methods = [SwitchCrossover], 
                 mutation_methods = [changeSubTreeMutation],
                 selection_method = partial(StochasticUniversalSampling,surviving= 5),
                 variable_set = treevolution.toolkit.variable_set,
                 terminal_set = treevolution.toolkit.terminal_set,
                 function_set = treevolution.toolkit.function_set
                 ):
            
        self.fitness = fitnessFunc
        self.size = size
        self.mindepth = mindepth
        self.maxdepth = maxdepth
        self.growing_methods = growing_methods
        self.crossover_methods = crossover_methods
        self.mutation_methods = mutation_methods
        self.selection_method = selection_method
        self.variable_set = variable_set.freshCopy()
        self.function_set = function_set.freshCopy()
        self.terminal_set = terminal_set.freshCopy()

        self.population=[]
        for i in range(self.size):
            self.population.append(self.randomTree())
                        
    def randomTree(self):
        growing_function = choice(self.growing_methods)
        return growing_function(self, self.maxdepth)
        
    def evolve(self, generations = 1, report = 1, plot = False, simplify = 0):
        for i in range(generations):
            for individual in self.population:
                currentFitness = self.fitness(individual)
                if individual.fitness != 0:
                    if individual.fitness > currentFitness:
                        self.function_set.batchChange(individual.getOccurrenceSet(), success = False)
                        self.variable_set.batchChange(individual.getOccurrenceSet(), success = False)
                        self.terminal_set.batchChange(individual.getOccurrenceSet(), success = False)
                    elif individual.fitness < currentFitness:
                        self.function_set.batchChange(individual.getOccurrenceSet(), success = True)
                        self.variable_set.batchChange(individual.getOccurrenceSet(), success = True)
                        self.terminal_set.batchChange(individual.getOccurrenceSet(), success = True)
                individual.fitness = currentFitness
            self.selection_method(self)
            if simplify is not 0:
                if i % simplify == 0:
                    for i in range(self.size):
                        self.population[i] = treevolution.toolkit.simplify(self.population[i])
            if (i+1) % report == 0:
                print 'Generation %d' % (i+1) 
                print 'Best fitness: %d' % self.bestFitness()
                
    def bestFitness(self):
        return max([self.fitness(t) for t in self.population])
    
    def bestIndividual(self):
        return sorted(self.population, key=lambda t: self.fitness(t),reverse=True)[0]

    def randomIndividual(self):
        return choice(self.population)
        
    def randomNode(self, parent):
        rchoice = (self.terminal_set+self.function_set+self.variable_set).randomElement()

        if rchoice.__class__ is Variable:
            return GPVariable(rchoice, parent=parent)
        if rchoice.__class__ is Function:
            return GPFunction(rchoice, parent=parent)
        else:
            return GPTree(rchoice, parent=parent)
        
    def randomTerminal(self, parent):
        rchoice = (self.variable_set+self.terminal_set).randomElement()
                
        if rchoice.__class__ is Variable:
            return GPVariable(rchoice, parent=parent)
        else:
            return GPTree(rchoice, parent=parent)
    
    def randomFunction(self, parent):
        
        return GPFunction(self.function_set.randomElement(), parent=parent)

    def randomCrossoverOperator(self):
        return choice(self.crossover_methods)
    
    def randomMutationOperator(self):
        return choice(self.mutation_methods)
    
    def addVariable(self, representation):
        self.variable_set.append(Variable(len(self.variable_set)-1, representation=representation))
        