import tellurium as te
import numpy as np


class Reaction():

    def __init__(self, ID):
        self.ID = ID
        # self.reactant1 = 0
        # self.reactant2 = 0
        # self.product1 = 0
        # self.product2 = 0
        # self.ratelaw = 0


class Species():

    def __init__(self, ID):
        self.ID = ID




class Edge():

    def __init__(self, source, dest, sign):
        self.source = source
        self.dest = dest
        self.sign = sign

    def printEdge(self):
        print(f"{self.source} -> {self.dest} ({self.sign})")

class Graph():

    def __init__(self, edges, nodes):
        # Allocate blank adjacency list
        self.adj = {}
        for node in nodes:
            self.adj[node.ID] = []
        # Add edges ... (?)
        for current in edges:
            self.adj[current.source].append((current.dest, current.sign))

    def printGraph(self):
        for entry in self.adj:
            print(f"{entry} -> {self.adj[entry]}")


astr = '''

X0 -> X1; k1*X0
X1 -> X0; k2*X1
X1 + X2 -> X2 + X2; k3*X1*X2
X2 -> X1; k4*X2
X0 = 2
X1 = 2
X2 = 3
k1 = 4
k2 = 2
k3 = 3
k4 = 1
'''

def getSpeciesReaction(list, ID):
    # This assumes that the ID is in the form letter-number, eg S1
    return list[int(ID[1])]


r = te.loada(astr)
speciesList = []
for i in range(r.getNumFloatingSpecies()):
    speciesList.append(Species(f'S{i}'))

reactionList = []
for i in range(r.getNumReactions()):
    reactionList.append(Reaction(f'J{i}'))



A = r.getFullStoichiometryMatrix()


reactionlist_full = []
lines = astr.splitlines()
for line in lines:
    if '->' in line and not line.startswith('#'):
        line = line.replace(' ', '')  # strip spaces
        # separate products and reactants by splitting at ->
        rxn = line.split('->')
        reactants = rxn[0]
        reactants = reactants.split("+")
        # Remove the rate constant part
        products = rxn[1].split(';')[0]
        products = products.split("+")
        ratelaw = rxn[1].split(';')[1]
        reactionlist_full.append([reactants, products, ratelaw])




#1. Draw edges based on stoichiometry matrix
## These edges will all originate from reaction nodes

edgeList = []
species, reaction = np.shape(A)
for j in range(reaction):
    for i in range(species):
        if A[i, j] != 0:
            if A[i, j] < 0:
                sign = -1
            elif A[i, j] > 0:
                sign = 1
            edgeList.append(Edge(reactionList[j].ID, speciesList[i].ID, sign))

#2. Draw edges based on rate laws
## These edges will all originate from species nodes,
## For now, I'm going to do this only with mass action laws.
for j in range(len(reactionlist_full)):
    # The sources are going to be the substrates (in all cases if we're using mass action
    for r in reactionlist_full[j][0]:
        # If the reactant is in the rate law (which it will be for now with mass action)
        if r in reactionlist_full[j][2]:
            source = getSpeciesReaction(speciesList, r).ID
            dest = reactionList[j].ID
            edge = Edge(source, dest, 1)
            edgeList.append(edge)





g = Graph(edgeList, speciesList + reactionList)

g.printGraph()













# r = te.loada('''
# var S0
# var S1
# var S2
# S2 -> S1; k1*S2
# S2 + S0 -> S0; k2*S2*S0
# S0 -> S2; k3*S0
# S2 -> S2+S2; k4*S2
# S1 -> S0+S2; k5*S1
# k1 = 4
# k0 = 1
# k2 = 4
# k3 = 8
# k4 = 146
# k5 = 16
# k6 = 2
# S0 = 1.0
# S1 = 5.0
# S2 = 9.0
# ''')

#m = r.simulate(0,1000,1000)
#r.plot()

# r = te.loada('''
# var S0
# var S1
# var S2
# S2 -> S1; k1*S2
# S2 + S0 -> S0; k2*S2*S0
# S0 -> S2; k3*S0
# S2 -> S2+S2; k4*S2
# S1 -> S0+S2; k5*S1
# k1 = 4
# k0 = 1
# k2 = 4
# k3 = 8
# k4 = 146
# k5 = 16
# k6 = 2
# S0 = 1.0
# S1 = 5.0
# S2 = 9.0
# ''')

#m = r.simulate(0,1000,1000)
#r.plot()
