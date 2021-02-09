import time
class Node: 
    def __init__(self, tag, size):
        self.tag = tag
        self.label = None
        self.neighbours = []
        self.distanceToEnd = None
        self.distanceFromStart = None
        self.distanceToOtherCities = []


def solver(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        global nodes, totalCities
        data = list(map(str.strip, f.readlines()))
        totalCities, totalRoads, start, end = data[0].split()
        totalCities, totalRoads, start, end = int(totalCities), int(totalRoads), int(start), int(end)
        nodes = []
        distanceToOtherCities = {}
        
        for i in range(int(totalCities)):
            nodes.append(Node(i, totalCities))
        for road in data[1: int(totalRoads) + 1]:
            city1, city2 = road.split()
            city1, city2 = int(city1), int(city2)
            addNeighbours(city1, city2)
        test1Cities, test2Cities = data[-2].split(), data[-1].split()
        allTestSites = test1Cities[1:] + test2Cities[1:]
        ShortestPath = 999999
        npath = None
        for city in allTestSites:
            path = 1
            if nodes[int(city)].distanceFromStart == None: 
                d = findShortestPath(start, int(city))
                nodes[int(city)].distanceFromStart = d
                path += d
            else:
                path += nodes[int(city)].distanceFromStart
            if path < ShortestPath:
                if city in test1Cities[1:]:
                    for city2 in test2Cities[1:]:
                        city2 = int(city2)
                        currCity = nodes[city2]
                        if (int(city), city2) not in distanceToOtherCities and (city2, int(city)) not in distanceToOtherCities:
                            path2 = findShortestPath(int(city), city2)
                            distanceToOtherCities[(int(city), city2)] = path2
                            distanceToOtherCities[(city2, int(city))] = path2
                        else:
                            path2 = distanceToOtherCities[(int(city), city2)]

                        if path + path2 > ShortestPath:
                            continue 
                        if currCity.distanceToEnd == None:
                            d3 = findShortestPath(int(city2), end)
                            path3 = d3
                            currCity.distanceToEnd = d3
                        else:
                            path3 = currCity.distanceToEnd
                        currPath = path + path2 + path3
                        if currPath < ShortestPath: 
                            ShortestPath = currPath
                            npath = [city, city2]
                elif city in test2Cities[1:]:
                    for city2 in test1Cities[1:]:
                        city2 = int(city2)
                        currCity = nodes[city2]
                        if (int(city), city2) not in distanceToOtherCities and (city2, int(city)) not in distanceToOtherCities:
                            path2 = findShortestPath(int(city), city2)
                            distanceToOtherCities[(int(city), city2)] = path2
                            distanceToOtherCities[(city2, int(city))] = path2
                        else:
                            path2 = distanceToOtherCities[(int(city), city2)]
                        if path + path2 > ShortestPath:
                            continue
                        if currCity.distanceToEnd == None:
                            d3 = findShortestPath(int(city2), end)
                            path3 = d3
                            currCity.distanceToEnd = d3
                        else:
                            path3 = currCity.distanceToEnd
                        currPath = path + path2 + path3
                        if currPath < ShortestPath: 
                            ShortestPath = currPath
                            npath = [city, city2]
        return ShortestPath


def addNeighbours(node1, node2):
    nodes[node1].neighbours.append(node2)
    nodes[node2].neighbours.append(node1)
    return 


def bfs(start, end, distance):
    queue = []
    visited = [False for i in range(totalCities)]
    visited[start] = True
    distance[start] = 0
    queue.append(start)
    while (len(queue) != 0):
        currNode = queue.pop(0)
        for i in nodes[currNode].neighbours: 
            if not visited[i]:
                visited[i] = True
                distance[i] = distance[currNode] + 1
                queue.append(i)
                if i == end:
                    return True         
    return False


def findShortestPath(start, end): 
    # previousNodes = [-1 for i in range(totalCities)]
    distance = [100000 for i in range(totalCities)]
    b = bfs(start, end, distance)
    if not b: 
        return None
    shortestPath = distance[end]
    return shortestPath


def DFS(node):        
    stack = []
    stack.append(node)
    node.visited = True
    leafDist = None
    while  len(stack) != 0:
        currNode = stack.pop()
        # currNode = nodes[nodeID]
        # print(currNode.id, end = " ") 
        for neigh in currNode.neighbours:
            if not nodes[neigh].visited:
                stack.append(nodes[neigh])
                nodes[neigh].visited = True
                nodes[neigh].distanceFromRoot = currNode.distanceFromRoot + 1 
                if nodes[neigh].isLeaf:
                    if leafDist == None:
                        leafDist = nodes[neigh].distanceFromRoot
                    else:
                        if nodes[neigh].distanceFromRoot != leafDist:
                            return False
    return True

def driver():
    for i in range(1, 11):
        inFile = "alg\giraffe\datapub\pub" + \
        f"{i:02d}" + '.in'
        outFile = "alg\giraffe\datapub\pub" + \
        f"{i:02d}" + '.out'
        t1 = time.time()
        myAns = solver(inFile)
        t2 = time.time()
        with open(outFile, 'r', encoding='utf-8') as out:
            ans = out.readlines()
            ans = list(map(str.strip, ans))
            ans = int(ans[0])
        print(myAns, '|', ans, '|' myAns == ans, 'time taken = ', t2 - t1)
       

driver()


            

