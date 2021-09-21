# A dependency-free version of networkx's implementation of Johnson's cycle finding algorithm
# Original implementation: https://github.com/networkx/networkx/blob/master/networkx/algorithms/cycles.py#L109
# Original paper: Donald B Johnson. "Finding all the elementary circuits of a directed graph." SIAM Journal on Computing. 1975.

from collections import defaultdict


def simple_cycles(G):
    # Yield every elementary cycle in python graph G exactly once
    # Expects a dictionary mapping from vertices to iterables of vertices

    # In my case, the iterables will be tuples (ID (str), sign (int)) and for now we only care about positive signs
    def _unblock(thisnode, blocked, B):
        stack = set([thisnode])
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    G = {v: set(nbrs) for (v, nbrs) in G.items()}  # make a copy of the graph
    sccs = strongly_connected_components(G)
    while sccs:
        scc = sccs.pop()
        startnode = scc.pop()
        path = [startnode]
        blocked = set()
        closed = set()
        blocked.add(startnode)
        B = defaultdict(set)
        stack = [(startnode, list(G[startnode]))]
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                    closed.update(path)
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, list(G[nextnode])))
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            if not nbrs:
                if thisnode in closed:
                    _unblock(thisnode, blocked, B)
                else:
                    for nbr in G[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
                path.pop()
        remove_node(G, startnode)
        H = subgraph(G, set(scc))
        sccs.extend(strongly_connected_components(H))


def strongly_connected_components(graph):
    # Tarjan's algorithm for finding SCC's
    # Robert Tarjan. "Depth-first search and linear graph algorithms." SIAM journal on computing. 1972.
    # Code by Dries Verdegem, November 2012
    # Downloaded from http://www.logarithmic.net/pfh/blog/01208083168

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
    for nbrs in G.values():
        nbrs.discard(target)


def subgraph(G, vertices):
    # Get the subgraph of G induced by set vertices
    # Expects values of G to be sets
    return {v: G[v] & vertices for v in vertices}
#
# #example:
# graph = {0: [7, 3, 5], 1: [2], 2: [7, 1], 3: [0, 5], 4: [6, 8], 5: [0, 3, 7], 6: [4, 8], 7: [0, 2, 5, 8], 8: [4, 6, 7]}
# print(tuple(simple_cycles(graph)))

g = {'S0': [('J0', 1)],
     'S1': [('J1', 1), ('J2', 1)],
     'S2': [('J2', 1), ('J3', 1)],
     'J0': [('S0', -1), ('S1', 1)],
     'J1': [('S0', 1), ('S1', -1)],
     'J2': [('S1', -1), ('S2', 1)],
     'J3': [('S1', 1), ('S2', -1)]}

# baby_g = {'S0' : [('S1', 1)],
#           'S1' : [('S2', 1)],
#           'S2' : [('S0', 1)]
#           }

scc = strongly_connected_components(g)