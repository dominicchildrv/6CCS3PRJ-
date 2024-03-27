#!/usr/bin/env python3

from graph import Graph
from booleanFormula import BooleanFormula
from graphConverter import cnf_to_graph
from mapEngine import *
from mapToLayout import *
from database import PacmanDatabase

graph = Graph()

graph.add_vertex("A")
graph.add_vertex("B")


graph.add_edge("A", "B")

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

map2 = generate_map(graph2)

list2 = map2.return_map()

for item in list2:
    print (item)

map = generate_map(graph)

list = map.return_map()

for item in list:
    print(item)



db = PacmanDatabase('pacman_layouts.db')

layout2 = Layout(map2, 4, db, 'smallMap')

layout2.save_layout()

print(layout2.return_layout())

# Retrieve and print a layout
layout = db.get_layout(layout2.get_name())
if layout:
    print(f"Retrieved layout: {layout}")
else:
    print("Layout not found.")
