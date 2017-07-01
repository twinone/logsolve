#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def getLinks(source,listWhite):
    """
    It returns the list of all the accessible cells
    from the one passed as source. listWhite are the walls of the board
    """
    i,j = source
    adjacents = []
    y, g = i, j
    while (y,g) not in listWhite:
        y += 1
    adjacents.append((y-1,g))
    y, g = i, j
    while (y,g) not in listWhite:
        y -= 1
    adjacents.append((y+1,g))
    y, g = i, j
    while (y,g) not in listWhite:
        g += 1
    adjacents.append((y,g-1))
    y, g = i, j
    while (y,g) not in listWhite:
        g -= 1
    adjacents.append((y,g+1))
    return set( [(a,b) for (a,b) in adjacents if (a,b) != (i,j)] )

def build_graph(dots,source):
    """
    Given the list of walls, it builds the adjacency list (dictionary)
    that represents the graph. Firstly, it adds the borders of the board to
    the listWhite list. Secondly, it loops over all the wall cells seeking
    free and accessible positions. Note that not all non-wall cells are
    accessible, since the agent must be always resting on a wall cell, at least.
    """
    graph = {}
    listWhite = [(0,j) for j in range(10)] + [(17,j) for j in range(10)]
    listWhite = listWhite + [(i,0) for i in range(1,17)] + \
                            [(i,9) for i in range(1,17)]
    listWhite = listWhite + dots
    free_positions = set()
    for (i,j) in listWhite:
        if i-1 > 0  and (i-1,j) not in listWhite: free_positions.add((i-1,j))
        if i+1 < 17 and (i+1,j) not in listWhite: free_positions.add((i+1,j))
        if j-1 > 0  and (i,j-1) not in listWhite: free_positions.add((i,j-1))
        if j+1 < 9  and (i,j+1) not in listWhite: free_positions.add((i,j+1))
    for pos in free_positions:
        graph[pos] = getLinks(pos,listWhite)

    if source in graph:
        graph[source].union(getLinks(source,listWhite))
    else:
        graph[source] = getLinks(source,listWhite)
    return graph, listWhite

def getConfig():
    """
    This is a stub. From this action the input problem has to be captured
    and translated into the three representative elements of the problem:
    the source cell, the target cell, and the list of non-boder wall cells.
    """
    source = (5,8)
    target = (3,6)
    whiteDots = [(1,1),(1,8),(2,3),(3,7),(4,8),(5,7),(6,2),(8,1),\
    (9,1),(9,6),(10,6),(12,7),(13,2),(15,2),(15,8),(16,6),(16,8)]
    return(source,target,whiteDots)

def pathIntoAction(path):
    """
    This is a stub. This action exemplifies how to translate from a found
    path into a plan to solve the problem physically.
    """
    actions = []
    for i in range(len(path)-1):
        i1,j1 = path[i]
        i2,j2 = path[i+1]
        if i2 < i1:
            actions.append('UP')
        elif i2 > i1:
            actions.append('DOWN')
        elif j2 > j1:
            actions.append('->')
        else:
            actions.append('<-')
    return actions

minRegisteredPath = list(range(100))
def getBestPathViaBacktracking(visited,currentPath,target,graph):
    """
    This action implements the classic branch and bound algorithm, following
    a Depth First Search structure. Note that, when the target is reached,
    there is no need of checking if the found path is shorter than the shortest
    so far, since longer paths won't be generated.
    """
    global minRegisteredPath
    if currentPath[-1] == target:
        minRegisteredPath = currentPath.copy()
    else:
        for adj in graph[currentPath[-1]]:
            if adj not in visited and len(currentPath) < len(minRegisteredPath):
                currentPath.append(adj)
                visited.add(adj)
                getBestPathViaBacktracking(visited,currentPath,target,graph)
                visited.remove(adj)
                currentPath.pop()

def printBeauty(list):
    for i in range(len(list)):
        print(i,list[i])

def main():
    """
    source: the starting cell
    target: the finishing cell
    dotsWhite: non-border wall cells
    listWhite: all wall cells in the board, including borders
    graph: relations of reachness between nodes
    """
    source, target, dotsWhite = getConfig()
    graph, listWhite = build_graph(dotsWhite,source)

    getBestPathViaBacktracking(set([source]),[source],target,graph)
    printBeauty(pathIntoAction(minRegisteredPath))

if __name__ == '__main__':
    main()
