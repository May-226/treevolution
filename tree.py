from random import choice, random, randint
from functools import partial

class GPTree:
    def __init__(self, nodetype, parent=None):
        self.type = nodetype
        self.parent = parent
        self.children=[]
        self.fitness = 0

    def __repr__(self):
        return '%s' % (self.type.representation)

    def __eq__(self,other):
        if self.type == other.type:
            return True
        else:
            return False        
        
    def evaluate(self, inputv):
        return self.type.value
    
    def randomSubTree(self):
        return self

    def clone(self):
        clone = GPTree(self.type)
        return clone

    def replaceBy(self,other):
        replacement = other.clone()
        replacement.parent = self.parent
        if replacement.parent is None:
            return replacement
        else:
            position = replacement.parent.children.index(self)
            replacement.parent.children.pop(position)
            replacement.parent.children.insert(position,other)

    def depth(self):
        return 1
    
    def getOccurrenceSet(self):
        return { self.type: 1}
    

class GPFunction(GPTree):
    def __init__(self, function, parent=None):
        self.children = []
        self.parent = parent
        self.type = function    
        self.fitness = 0

    def __repr__(self):
        repres = '(%s' % self.type.representation
        for child in self.children:
            repres += ' %s' % child
        repres += ')'
        return repres
    
    def __eq__(self, other):
        if self.type == other.type and self.children == other.children:
            return True
        else:
            return False

    def addChild(self,other):
        self.children.append(other)
        
    def removeChild(self,other):
        self.children.remove(other)

    def evaluate(self, inputv):
        finalfunc = self.type.value
        
        if len(self.children) != self.type.nArgs:
            print "Not enough arguments!"
            return
        
        for argument in self.children[:1]:
            finalfunc = partial(finalfunc, argument.evaluate(inputv))
        try:
            return finalfunc(self.children[len(self.children)-1].evaluate(inputv))
        except ZeroDivisionError:
            return 1
            raise
        
    def randomSubTree(self):
        if self.type.nArgs == 0:
            return self
        
        if random()>0.5:
            return choice(self.children).randomSubTree()
        else:
            return self
        
    def clone(self):
        clone = GPFunction(self.type)
        for child in self.children:
            clone.children.append(child.clone())
        return clone

    def depth(self):
        return 1+max([child.depth() for child in self.children])
    
    def getOccurrenceSet(self):
        occurrenceSet = { self.type : 1 }
        for child in self.children:
            childSet = child.getOccurrenceSet()
            for element in childSet.keys():
                if element in occurrenceSet.keys():
                    occurrenceSet[element]+=1
                else:
                    occurrenceSet[element]=childSet[element]
        return occurrenceSet
                
class GPVariable(GPTree):
    def __init__(self, variable, parent=None):
        GPTree.__init__(self,variable, parent=parent)
        self.ninput = self.type.ninput
        self.fitness = 0

    def evaluate(self,inputv):
        return inputv[self.ninput]

    def clone(self):
        return GPVariable(self.type)
