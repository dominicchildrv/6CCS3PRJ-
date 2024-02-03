from graph import Graph
from booleanFormula import BooleanFormula

def cnf_to_graph(formula):
    graph = Graph()
    
    # Add vertices to the graph for each literal in the formula
    for clause in formula.return_clause_list():
        for literal in clause:
            graph.add_vertex(literal)

        # Add edges between literals in the same clause
        # We can do this by adding edges between consecutive literals in the clause
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):
                graph.add_edge(clause[i], clause[j])

    return graph
