# A dependency-free version of networkx's implementation of Johnson's cycle finding algorithm
# Original implementation: https://github.com/networkx/networkx/blob/master/networkx/algorithms/cycles.py#L109
# Original paper: Donald B Johnson. "Finding all the elementary circuits of a directed graph." SIAM Journal on Computing. 1975.
from copy import deepcopy
from collections import defaultdict


def simple_cycles(G):
    # Yield every elementary cycle in python graph G exactly once
    # Expects a dictionary mapping from vertices to iterables of vertices
    def _unblock(thisnode, blocked, blockedMap):
        stack = set([thisnode])
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                # Check if it's in the blocked Map, remove it, continue until the entire "chain" is removed
                while node in list(blockedMap.keys()):
                    stack.update(blockedMap[node]) #add it to stack
                    nextnode = blockedMap[node]
                    blockedMap[node].clear() # remove it from map
                    node = nextnode

    allCycles = []
    G = {v: set(nbrs) for (v,nbrs) in G.items()} # make a copy of the graph
    sccs = strongly_connected_components(G) # This is a list of the strongly connected components
    while sccs:
        scc = sccs.pop()  # Take a strongly connected conmponent off the list
        # ADDED BY ME: Make a subgraph of the connected component
        subG = subgraph(G, scc)
        startnode = scc.pop()
        path=[startnode]
        blockedSet = set() # Blocked set ?
        closed = set() #Not sure what this is
        blockedSet.add(startnode)
        blockedMap = {}
        stack = [ (startnode,list(subG[startnode])) ]
        while stack:
            thisnode, nbrs = stack[-1] # nbrs will be a list of node tuples that thisnode connects to
            if nbrs: #If there are (still) neighbors, pop off one and check it it's the start node.
                nextnode = nbrs.pop()
                weight = nextnode[1]
                if weight < 0:
                    continue
                nextnode = nextnode[0]
                if nextnode == startnode: # If the neighbor is the start node, then we've found a cycle.
                    allCycles.append(deepcopy(path))
                    yield path[:]

                    closed.update(path)
                elif nextnode not in blockedSet: # Otherwise, check it it's in the blocked set, if not, add it to the blocked set and pth(?)
                    path.append(nextnode)
                    stack.append((nextnode, list(subG[nextnode])))
                    closed.discard(nextnode) # Notsure
                    blockedSet.add(nextnode)
                    continue
            if not nbrs:

                if thisnode in closed: # When do we unblock nodes?
                    _unblock(thisnode, blockedSet, blockedMap)
                else:
                    for nbr in subG[thisnode]:
                        if nbr[0] not in blockedMap.keys():
                            blockedMap[nbr[0]] = {thisnode}
                        elif thisnode not in blockedMap[nbr[0]]:
                            blockedMap[nbr[0]].add(thisnode)
                stack.pop()
                path.pop()
        H = remove_node(subG, startnode) # Remove the fully explored node from the subgraph of the strongly connected comp.
        # H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H)) # add the subgraph of the strongly connected component to the sccs list

def strongly_connected_components(graph):
    # Tarjan's algorithm for finding SCC's
    # Robert Tarjan. "Depth-first search and linear graph algorithms." SIAM journal on computing. 1972.
    # Modified from code by Dries Verdegem, November 2012

    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []

    # in my case, a node is (ID (str), sign (int))
    def _strong_connect(node):
        index[node] = index_counter[0] # Dictionary of integer node IDs
        lowlink[node] = index_counter[0] # Initialize node's lowlink to be itself, again using the string ID as key
        index_counter[0] += 1 # The next node will be labeled with the subsequent integer
        stack.append(node)

        successors = graph[node] # This is the list of tuples that the node connects to, it is a list of TUPLES
        for successor in successors:
            # Skip the edge if it's negative
            if successor[1] < 0:
                continue
            # If we have never seen this node before, label it and add it to the stack. Assessing lowLink
            if successor[0] not in index:
                _strong_connect(successor[0])
                lowlink[node] = min(lowlink[node], lowlink[successor[0]])
            # If we have seen the node before, update it's lowlink
            elif successor[0] in stack:
                lowlink[node] = min(lowlink[node], index[successor[0]])

        # If we get through the loop and the node's lowlink is still itself, then we have a strongly connected component
        if lowlink[node] == index[node]:
            connected_component = []
            # Pop nodes off the stack and add to scc until we get to original node
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component[:])

    for node in graph:
        if node not in index:
            _strong_connect(node)

    return result


def remove_node(G, target):
    # Completely remove a node from the graph
    # Expects values of G to be sets
    del G[target]
    newG = deepcopy(G)
    for key in G.keys():
        newG[key] = set()
        for nbr in G[key]:
            if nbr[0] != target:
                newG[key].add(nbr)
    del G
    return newG

def subgraph(G, vertices):
    # Get the subgraph of G induced by set vertices, in other words, get the graph of a stongly connected coponent
    # Expects values of G to be sets
    # if len(vertices) <= 1: #Ignore single node subgraphs because they cannot have cycles
    #     return None
    subgraph = {}
    for v in vertices:
        neighbors = set()
        for edge in G[v]:
            if edge[0] in vertices:
                neighbors.add(edge)
        subgraph[v] = neighbors
    return subgraph


######### TESTS ##########
# g = {'S0': [('J0', 1)],
#      'S1': [('J1', 1), ('J2', 1)],
#      'S2': [('J2', 1), ('J3', 1)],
#      'J0': [('S0', -1), ('S1', 1)],
#      'J1': [('S0', 1), ('S1', -1)],
#      'J2': [('S1', -1), ('S2', 1)],
#      'J3': [('S1', 1), ('S2', -1)]}

# sample_g = {'S1': {('S2', 1), ('S5', 1), ('S8', 1)},
#             'S2': {('S7', 1), ('S3', 1), ('S9', 1)},
#             'S3': {('S1', 1), ('S2', 1), ('S4', 1), ('S6', 1)},
#             'S4': {('S5', 1)},
#             'S5': {('S2', 1)},
#             'S6': {('S4', 1)},
#             'S7': {},
#             'S8': {('S9', 1)},
#             'S9': {('S8', 1)}
#             }

# baby_g = {'S0' : [('S1', 1)],
#           'S1' : [('S2', 1)],
#           'S2' : [('S0', 1)]
#           }

# scc = strongly_connected_components(sample_g)[2]

# print(tuple(simple_cycles(g)))
