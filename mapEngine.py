
from graph import Graph

class PacmanMap:

    def __init__(self) -> None:
        
        self.start = StartGadget()
        self.end = EndGadget()
        self.tail = self.start

    def return_start(self):

        return self.start
    
    def return_end(self):

        return self.end
    
    def return_tail(self):

        return self.tail
    
    def add_to_map(self, gadget):
        
        self.tail.set_tail(gadget)
        gadget.set_head(self.tail)
        self.tail = gadget

    def set_end(self):

        self.tail.set_tail(self.end)
        self.end.set_head(self.tail)

    def return_map(self) -> list:
        map_sequence = [self.start]
        current_gadget = self.start

        while current_gadget.tail is not None:
            current_gadget = current_gadget.tail
            map_sequence.append(current_gadget)

        return map_sequence
    
    
    
    def max_rooms_in_connection(self) -> int:
        max_rooms = 0
        current_gadget = self.start

        while current_gadget is not None:
            # Check if the current gadget is a ConnectionGadget
            if isinstance(current_gadget, ConnectionGadget):
                # Update max_rooms if the current gadget has more rooms
                max_rooms = max(max_rooms, current_gadget.count_rooms())
            
            # Move to the next gadget in the map
            current_gadget = current_gadget.tail

        return max_rooms
    

    






class StartGadget:

    def __init__(self) -> None:

        self.tail = None


    def set_tail(self, tail_gadget):

        self.tail = tail_gadget


    def return_tail(self):

        return self.tail
        
        




class EndGadget:

    def __init__(self) -> None:
        
        self.head = None
        self.tail = None


    def set_head(self, head_gadget):

        self.head = head_gadget

    def return_head(self):

        return self.head






class TollRoadGadget:

    def __init__(self) -> None:

        self.head = None
        self.tail = None

    def set_head(self, head_gadget):

        self.head = head_gadget


    def set_tail(self, tail_gadget):

        self.tail = tail_gadget

    def return_head(self):

        return self.head
    
    def return_tail(self):

        return self.tail







class ConnectionGadget:

    def __init__(self) -> None:
        
        self.head = None
        self.tail = None
        self.body = []

    def set_head(self, head_gadget):

        self.head = head_gadget


    def set_tail(self, tail_gadget):

        self.tail = tail_gadget


    def add_to_body(self, room_gadget):

        self.body.append(room_gadget)


    def count_rooms(self):

        return len(self.body)




class RoomGadget:

    def __init__(self, name) -> None:
        
        self.vertex = None
        self.name = name

    def set_vertex(self, vertex):

        self.vertex = vertex

    


def generate_map(graph: Graph) -> PacmanMap:
    pacman_map = PacmanMap()
    
    # Step 1: Create ConnectionGadget instances for each vertex
    for vertex in graph.graph:
        connection_gadget = ConnectionGadget()
        pacman_map.add_to_map(connection_gadget)

        # Step 2: Add RoomGadget instances for each neighbor
        for neighbor in graph.graph[vertex]:
            room_gadget = RoomGadget(name=neighbor)
            connection_gadget.add_to_body(room_gadget)

        tollRoad = TollRoadGadget()
        pacman_map.add_to_map(tollRoad)


    # Step 3: Set the end gadget after all connection gadgets are added
    pacman_map.set_end()

    return pacman_map




