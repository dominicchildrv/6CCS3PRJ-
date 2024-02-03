#!/usr/bin/env python3

from graph import Graph
from booleanFormula import BooleanFormula
from graphConverter import cnf_to_graph

graph = Graph()

graph.add_vertex("A")
graph.add_vertex("B")
graph.add_vertex("C")

graph.add_edge("A", "B")
graph.add_edge("C", "B")

graph.display_graph()



cnf = BooleanFormula()

cnf.add_clause("A","B")
cnf.add_clause("A","C")
cnf.add_clause("A","B")
cnf.add_clause("A","B", "D")
cnf.add_clause("B","C")
cnf.add_clause("A","D", "B")

cnf.print_formula()


cnf.print_clause_list()

graph2 = cnf_to_graph(cnf)

graph2.display_graph()