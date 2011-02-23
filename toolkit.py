from treevolution.nodetype import *
from treevolution.tree import *
from math import pow
from prob_set import prob_set

Zero = Nodetype(0)
One = Nodetype(1)

XVar = Variable(1,'X')
YVar = Variable(2,'Y')

def simplify(tree):
    original_type = tree.type
    if tree.__class__ is GPFunction:
        for i in range(len(tree.children)):
            temp = tree.children[i]
            tree.children[i] = simplify(temp)
        for rule in tree.type.rules:
            if tree.type is original_type:
                tree = rule(tree)
    return tree
    
def makeIdentityRule(nodetype):
    return partial(IdentityElement, nodetype)

def makeAbsorbingRule(nodetype):
    return partial(AbsorbingElement, nodetype)

def IdentityElement(nodetype, tree):
    if nodetype in [child.type for child in tree.children]:
        for child in tree.children:
            if child.type is not nodetype:
                return child
        return GPTree(nodetype, parent = tree.parent)
    return tree

def AbsorbingElement(nodetype, tree):
    if nodetype in [child.type for child in tree.children]:
        return GPTree(nodetype, parent=tree.parent)
    return tree

def SubstractionIdentityElement(tree):
    if tree.children[1].type is Zero:
        return tree.children[0]
    return tree

def CancelingElement(tree): 
    if tree.children[0] == tree.children[1]:
        return GPTree(Zero, parent=tree.parent)
    return tree

Addition = Function(lambda x,y: x+y, '+',
                    rules = [makeIdentityRule(Zero)])

Substraction = Function(lambda x,y: x-y, '-',
                        rules = [SubstractionIdentityElement, CancelingElement])

Multiplication = Function(lambda x,y: x*y, '*', 
                          rules = [makeIdentityRule(One), makeAbsorbingRule(Zero)])

Power = Function(lambda x, y: pow(x,y), '^')

function_set = prob_set([Addition, Substraction, Multiplication])
terminal_set = prob_set([Zero, One])
variable_set = prob_set([XVar])