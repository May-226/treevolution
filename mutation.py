from inspect import getargspec

class Nodetype:
    def __init__(self, value, representation = ''):
        if representation == '':
            self.representation = str(value)
        else:
            self.representation = representation

        self.value = value

    def __repr__(self):
        return self.representation
    
    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False
                
    def __hash__(self):
        return hash(self.value)
    
    
class Function(Nodetype):
    def __init__(self,function,representation='', rules=[]):
        self.representation=representation
        self.value = function
        self.nArgs = len(getargspec(self.value)[0])
        self.rules = rules

class Variable(Nodetype):
    def __init__(self, ninput, representation = 'X'):
        Nodetype.__init__(self,None,representation)
        self.ninput = ninput-1
        
class Composite(Nodetype):
    def __init__(self, original_tree):
        
        Nodetype.__init__(self, representation=original_tree.__repr__)
        