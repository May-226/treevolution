from evolver import *
from toolkit import simplify, Multiplication
from selection import ElitistSelection, StochasticUniversalSampling

def fitness(tree):
    fit = 0
    for data in generateDataSet(lambda x: 2*x+1+x, 50):
        if tree.evaluate(data[0])==data[1]:
            fit+=1
    return fit
    
def generateDataSet(func, length):
    d=[]
    for i in range(length):
        temp = ([i],func(i))
        d.append(temp)
    return d

import scipy
from scipy.stats.stats import ttest_ind

if __name__ == "__main__": 
    results = [[],[]]
    for i in range(15):
        ga = evolver(fitnessFunc = fitness, maxdepth=5)
        ga.evolve(generations=100, report=299)
        print ga.bestFitness()
        print ga.function_set, ga.variable_set, ga.terminal_set
    
        
        
    '''
        ga2 = evolver(fitnessFunc = fitness, selection_method = ElitistSelection)
        ga2.evolve(generations=100, report=12323)
        results[0].append(ga.bestFitness())
        results[1].append(ga2.bestFitness())
    
    print results[0]
    print results[1]
    a = scipy.array(results[0])
    b = scipy.array(results[1])
    
    print ttest_ind(a,b)
    
'''


