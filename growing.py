from random import random

def grow(gevolver, depth, parent=None):
    
    tree = gevolver.randomFunction(parent)
    
    if depth==1:
        for i in range(tree.type.nArgs):
            tree.addChild(gevolver.randomTerminal(parent))
    else:
        for i in range(tree.type.nArgs):
            if random()>0.5:
                tree.addChild(grow(gevolver, depth-1, parent=tree))
            else:
                tree.addChild(grow(gevolver, depth-1, parent=tree))
                
    return tree

def full(gevolver, depth, parent=None):
    
    tree = gevolver.randomFunction(parent)
    
    if depth==1:
        for i in range(tree.type.nArgs):
            tree.addChild(gevolver.randomTerminal(parent))
    else:
        for i in range(tree.type.nArgs):
            tree.addChild(full(gevolver, depth-1, parent=tree))

    return tree    
