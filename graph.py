#Custom Graph datatype

class Graph:

    def __init__(self):
        #Graph will be represented as a dict
        self.graph = {}

    def add_vertex(self, vertex):
        #Checks if vertex is already in graph
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
            #checks both vertexes are in graph
            if vertex1 in self.graph and vertex2 in self.graph:
                 self.graph[vertex1].append(vertex2)
                 self.graph[vertex2].append(vertex1)

    def display_graph(self):
        #prints graph vertexes and edges
        for vertex, neighbors in self.graph.items():
            print(f"{vertex}: {', '.join(map(str, neighbors))}")
