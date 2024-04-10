from mapEngine import *
import random
import os
from database import PacmanDatabase


# Class for layouts, which represent and hold information about the Pacman maze
class Layout:

    def __init__(self, map: PacmanMap, ghosts: int, db:PacmanDatabase, name: str) -> None:

        self.name = name
        self.db = db 
        if ghosts > 4:
            raise ValueError("A maximum of 4 ghosts are allowed.")
        self.map = map
        self.layout = ''
        if map.max_rooms_in_connection() == 0:
            self.maxRooms =1
        else:
            self.maxRooms = map.max_rooms_in_connection()
        if self.get_width() == 0:
            self.maxWidth = 1
        else:
            self.maxWidth = self.get_width()
        self.numOfGhosts = ghosts
        self.generate_layout()  # Automatically generate the layout upon initialization


    # Generates the layout string so a .lay file can be made and saved
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


    # Add first layer of walls
    def add_start(self):
        self.layout += '%' * self.maxWidth + '\n'

    # Creates sets of connected rooms filled with pellets
    def add_connection(self, numOfRooms: int):
        baseLayer = '%...' * numOfRooms + (self.maxWidth - len('%...' * numOfRooms)) * '%' 
        lowerLayer = '%' + ('...' * numOfRooms) + ('.' * (numOfRooms - 1))
        lowerLayerPadding = (self.maxWidth - len(lowerLayer)) * '%'
        lowerLayer += lowerLayerPadding
        self.layout += baseLayer + '\n' + lowerLayer + '\n'

    # Creates an empty corridor where ghosts can spawn
    # Also places a power pellet (token) at the entrance
    def add_tollRoad(self):
        topLayer = '%' * 2 + 'o' + (self.maxWidth - 3) * '%'
        midLayer = '%' + ' ' * (self.maxWidth - 2) + '%'
        self.layout += topLayer + '\n' + midLayer + '\n'

    # Add the last layer of walls
    def add_end(self):
        self.layout += '%' * self.maxWidth + '\n'

    def get_width(self):
        # Calculate and return the width of the layout
        return ((4 * self.maxRooms) + 1)

    def return_layout(self):
        # Return the generated layout
        return self.layout
    

    # Function to add Pacman to the top of the layout
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
                # If the line is not long enough, it's an edge case
                pass

        # Reassemble the layout from the modified lines list
        self.layout = '\n'.join(lines) + '\n'



    # Function to randomly add ghosts to free spaces
    def add_ghosts(self):
        # Split the current layout into lines
        lines = self.layout.splitlines()

        # Find all possible positions for placing ghosts (empty spaces)
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

    
    # Function that creates a file holding the layout string
    def save_layout_to_file(self):
        # Define the path to the file
        file_path = os.path.join('pacman_utils', 'layouts', self.name + '.lay')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open the file for writing (overwrites if exists)
        with open(file_path, 'w') as file:
            file.write(self.layout)

        print(f"Layout saved to {file_path}.")

    
    # Save the layout to the database with the name and number of ghosts
    def save_layout_to_db(self):
        layout_id = self.db.insert_layout(self.name, self.numOfGhosts)
        print(f"Inserted layout with ID {layout_id}")

    def save_layout(self):

        #Update the layout name to avoid duplicates by appending a number to the name
        original_name = self.name
        i = 1
        while self.db.layout_name_exists(self.name):
            self.name = f"{original_name}{i}"
            i += 1

        self.save_layout_to_file()
        self.save_layout_to_db()

    
    def get_ghosts(self) -> int:

        return self.numOfGhosts
    
    def get_name(self) -> str:

        return self.name
    
    def get_string_length(self):

        partLayout = self.layout.split('\n')

        return len(partLayout[0])
    
    def get_string_height(self):

        partLayout = self.layout.split('\n')

        return len(partLayout)

