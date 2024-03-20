from mapEngine import *


class Layout:

    def __init__(self, map) -> None:
        
        self.map = map
        self.layout = ''
        self.maxRooms = map.max_rooms_in_connection()
        self.maxWidth = self.get_width()

    def add_start(self):

        pass

    def add_connection(self):

        pass

    def add_tollRoad(self):

        pass

    def add_end(self):

        pass

    def get_width(self):

        if (self.maxRooms == 1):
            return 5
        else:
            return (5 + (4*self.maxRooms))