import copy

class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.color = None

    def addNeighbour(self, neighbour):
        if neighbour not in self.neighbours:
            self.neighbours.append(neighbour)
            neighbour.neighbours.append(self)
        
    def addNeighbours(self, neighbours):
        for neighbour in neighbours:
            self.addNeighbour(neighbour)

    def removeNeighbour(self, neighbour):
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)
            neighbour.neighbours.remove(self)

    def removeNeighbours(self, neighbours):
        for neighbour in neighbours:
            self.removeNeighbour(neighbour)

    def hasEdge(self, vertex_to):
        return vertex_to in self.neighbours

    def getDegree(self):
        return len(self.neighbours)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

'''
A Graph has a dictionary whose key is a vertex name and its value a list of vertices, that represent edges
It is a undirected graph, meaning that A -> B  <=>  B -> A.
This is taken into consideration as vertices[A] will contain B and vertices[B] will contain A.
'''
class Graph:
    def __init__(self, vertices = {}):
        self.vertices = copy.deepcopy(vertices)
        self.name_to_original = {}
        self.name_to_current = {}
        for vertex in vertices:
            self.name_to_original[vertex.name] = vertex
        for vertex in self.vertices:
            self.name_to_current[vertex.name] = vertex

    def addVertex(self, vertex):
        self.vertices[vertex] = vertex.neighbours
        self.name_to_current[vertex.name] = vertex

    def addVertices(self, vertices):
        for vertex in vertices:
            self.addVertex(vertex)

    def addEdge(self, vertex_from, vertex_to):
        vertex_from.addNeighbour(vertex_to)
        self.vertices[vertex_from] = vertex_from.neighbours
        self.vertices[vertex_to] = vertex_to.neighbours

    def addEdges(self, edges):
        for edge in edges:
            self.addEdge(edge[0],edge[1])

    def removeVertex(self, vertex):
        while(self.vertices[vertex]):
            self.removeEdge(vertex, self.vertices[vertex][0])
        del self.name_to_current[vertex.name]
        del self.vertices[vertex]

    def removeVertices(self, vertices):
        for vertex in vertices:
            self.removeVertex(vertex)

    def removeEdge(self, vertex_from, vertex_to):
        vertex_from.removeNeighbour(vertex_to)
        self.vertices[vertex_from] = vertex_from.neighbours
        self.vertices[vertex_to] = vertex_to.neighbours

    def removeEdges(self, edges):
        for edge in edges:
            self.removeEdge(edge[0],edge[1])

    def hasEdge(self, vertex_from, vertex_to):
        if vertex_from in self.vertices:
            return vertex_from.hasEdge(vertex_to)
        return False

    def getDegree(self, vertex):
        if vertex in self.vertices:
            return vertex.getDegree()
        return False

    def show(self):
        for key in self.vertices.keys():
            print(str(key),
            "(" + str(key.color) + ")" if key.color is not None else "",
            "->", str(self.vertices[key]))
        print()

def graphColoring(in_graph, n):
    graph = Graph(in_graph.vertices)
    vertex_stack = list()
    while(graph.vertices):
        cut_vertex = None
        for vertex in list(graph.vertices):
            if vertex.getDegree() >= n:
                continue
            cut_vertex = vertex
            graph.removeVertex(cut_vertex)
            vertex_stack.append(cut_vertex)
            #print("Removed ", cut_vertex)
            #graph.show()
            #print(vertex_stack)

        if cut_vertex is None:
            print("Graph coloring is impossible with %d colors!" % n)
            return None
    #print("Graph coloring is possible with %d colors!" % n)
    while(vertex_stack):
        vertex_to_color = vertex_stack.pop()
        graph.addVertex(vertex_to_color)

        #print("Coloring ", vertex_to_color)

        original_vertex = graph.name_to_original[vertex_to_color.name]

        for vertex_to in in_graph.vertices[original_vertex]:
            if vertex_to.name in graph.name_to_current:
                new_vertex_to = graph.name_to_current[vertex_to.name]
                graph.addEdge(vertex_to_color, new_vertex_to)

        available_colors = list(range(n))
        for vertex_to_color_neighbour in vertex_to_color.neighbours:
            if vertex_to_color_neighbour.color is not None:
                if vertex_to_color_neighbour.color in available_colors:
                    available_colors.remove(vertex_to_color_neighbour.color)
        if available_colors:
            vertex_to_color.color = available_colors[0]

        #print("Colored ", vertex_to_color, " with ", vertex_to_color.color)
        #print(vertex_stack)
        #graph.show()
    print("Colored:")
    graph.show()
    return graph


# Test
a = Vertex('A')
b = Vertex('B')
c = Vertex('C')
d = Vertex('D')
e = Vertex('E')

a.addNeighbours([b,c,e])
b.addNeighbours([a,c])
c.addNeighbours([b,d,a,e])
d.addNeighbour(c)
e.addNeighbours([a,c])

g = Graph()
g.addVertices([a,b,c,d,e])
g.addEdge(b,d)
#g.show()

g.removeVertex(b)
print("Original:")
g.show()

graphColoring(g,3)
