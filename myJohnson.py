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

baby_g = {'S0' : [('S1', 1)],
          'S1' : [('S2', 1)],
          'S2' : [('S0', 1)]
          }

sample_g = {'S1': [('S2', 1), ('S8', 1)],
            'S2': [('S7', 1), ('S3', 1), ('S9', 1)],
            'S3': [('S1', 1), ('S2', 1), ('S4', 1), ('S6', 1)],
            'S4': [('S5', 1)],
            'S5': [('S2', 1)],
            'S6': [('S4', 1)],
            'S7': [],
            'S8': [('S9', 1)],
            'S9': [('S8', 1)]
            }

print(strongly_connected_components(sample_g))