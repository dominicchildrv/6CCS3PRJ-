from mapEngine import *
import random


class Layout:

    def __init__(self, map: PacmanMap, ghosts: int) -> None:

        if ghosts > 4:
            raise ValueError("A maximum of 4 ghosts are allowed.")
        self.map = map
        self.layout = ''
        self.maxRooms = map.max_rooms_in_connection()
        self.maxWidth = self.get_width()
        self.numOfGhosts = ghosts
        self.generate_layout()  # Automatically generate the layout upon initialization

    def generate_layout(self):
        # Add the start of the map layout
        self.add_start()

        # Iterate through the map to build the layout
        for gadget in self.map.return_map():
            if isinstance(gadget, StartGadget):
                # StartGadget handling is already done with add_start
                continue
            elif isinstance(gadget, ConnectionGadget):
                # Add a connection based on the number of rooms
                self.add_connection(len(gadget.body))
            elif isinstance(gadget, TollRoadGadget):
                # Add a toll road to the layout
                self.add_tollRoad()
            elif isinstance(gadget, EndGadget):
                # Add the end of the map layout
                self.add_end()
                break  # EndGadget should be the last, exit the loop

        self.add_pacman()
        self.add_ghosts()

    def add_start(self):
        self.layout += '%' * self.maxWidth + '\n'

    def add_connection(self, numOfRooms: int):
        baseLayer = '%...' * numOfRooms + (self.maxWidth - len('%...' * numOfRooms)) * '%' 
        lowerLayer = '%' + ('...' * numOfRooms) + ('.' * (numOfRooms - 1))
        lowerLayerPadding = (self.maxWidth - len(lowerLayer)) * '%'
        lowerLayer += lowerLayerPadding
        self.layout += baseLayer + '\n' + lowerLayer + '\n'

    def add_tollRoad(self):
        topLayer = '%' * 2 + 'o' + (self.maxWidth - 3) * '%'
        midLayer = '%' + ' ' * (self.maxWidth - 2) + '%'
        self.layout += topLayer + '\n' + midLayer + '\n' + midLayer + '\n'

    def add_end(self):
        self.layout += '%' * self.maxWidth + '\n'

    def get_width(self):
        # Calculate and return the width of the layout
        return ((4 * self.maxRooms) + 1)

    def return_layout(self):
        # Return the generated layout
        return self.layout
    
    def add_pacman(self):
        # Split the current layout into lines
        lines = self.layout.splitlines()

        # Ensure there's a second line to modify
        if len(lines) > 1:
            # Replace the third character (index 2) of the second line with 'P'
            # Ensure the line is long enough
            if len(lines[1]) >= 3:
                # Replace character with 'P', preserving the rest of the line
                lines[1] = lines[1][:2] + 'P' + lines[1][3:]
            else:
                # If the line is not long enough, it's an edge case,
                # Handle accordingly, maybe log a warning or extend the line
                pass

        # Reassemble the layout from the modified lines list
        self.layout = '\n'.join(lines) + '\n'


    def add_ghosts(self):
        # Split the current layout into lines
        lines = self.layout.splitlines()

        # Find all possible positions for placing ghosts (i.e., blank spaces)
        blank_positions = [
            (row_idx, col_idx) 
            for row_idx, line in enumerate(lines) 
            for col_idx, char in enumerate(line) 
            if char == ' '
        ]

        # Ensure there are enough blank spaces to place all ghosts
        if len(blank_positions) < self.numOfGhosts:
            print("Not enough space to add all ghosts!")
            return

        # Randomly select positions to place ghosts
        ghost_positions = random.sample(blank_positions, self.numOfGhosts)

        # Place ghosts in the selected positions
        for row_idx, col_idx in ghost_positions:
            line = list(lines[row_idx])  # Convert the string to a list for mutation
            line[col_idx] = 'G'  # Place ghost
            lines[row_idx] = ''.join(line)  # Convert the list back to a string

        # Reassemble the layout from the modified lines list
        self.layout = '\n'.join(lines) + '\n'