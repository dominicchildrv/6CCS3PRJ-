#!/usr/bin/env python3

from mapEngine import *

map = PacmanMap()

connection1 = ConnectionGadget()
toll1 = TollRoadGadget()
connection2 = ConnectionGadget()

map.add_to_map(connection1)
map.add_to_map(toll1)
map.add_to_map(connection2)
map.set_end()

list = map.return_map()

print(list)