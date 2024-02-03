class Graph:
    def __init__(self):
        # Graph will be represented as a dictionary
        self.graph = {}

    def add_vertex(self, vertex):
        # Checks if vertex is already in the graph
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        # Checks both vertices are in the graph
        if vertex1 in self.graph and vertex2 in self.graph:
            # Adds edge only if it doesn't already exist
            if vertex2 not in self.graph[vertex1]:
                self.graph[vertex1].append(vertex2)
            if vertex1 not in self.graph[vertex2]:
                self.graph[vertex2].append(vertex1)

    def display_graph(self):
        # Prints graph vertices and edges
        for vertex, neighbors in self.graph.items():
            print(f"{vertex}: {', '.join(map(str, neighbors))}")
