def SwitchCrossover(father, mother):
    child = father.clone()
    
    fatherPart = child.randomSubTree()
    motherPart = mother.randomSubTree()
    
    return fatherPart.replaceBy(motherPart)
