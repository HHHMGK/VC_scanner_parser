import os
import csv
from .constrant import OUTPUT_DIR
class Ulits:
    def __init__(self, _inut_path : str) -> None:
        
        # Read the transition table
        self.data = list(csv.reader(open("transition_table.csv")))
        
        # Turn data from transition_table into maps
        self.maps_state, self.maps_key = self.get_maps(self.data)

        # Create output path
        try:
            os.makedirs(OUTPUT_DIR) # Creates directories if they don't exist
        except OSError as e:
            if os.path.isdir(OUTPUT_DIR): 
                print(f"Folder '{OUTPUT_DIR}' already exists. ")
            else:
                print(f"Error creating folder: {e}")
        
    def get_maps(self, data: list):
        """
        The data from the transition table can be transformed:
         - The initial row represents "characters" , 
         - The initial column represents "states" 
         - The remaining cells represent transition states.
        Args:
            data (list): data get from transition_table.csv
        """
        data = list(csv.reader(open("trans.csv")))
        map_state = {}  # Map for states (row)
        map_key = {}  # Map for keys (column)

        # Insert to map_key
        for i in range(len(data[0])):  
            map_key[data[0][i]] = i

        # Insert to map_state
        for i in range(len(data)):  
            map_state[data[i][0]] = i

        return(map_state, map_key)
    def get_next_state(self, state, key):
        """
        Get the next state from the current state and the character (key).
        Args:
            state(str): the current state of the string
            key ( int ): the number present for character in map_key
        """
        return self.data[self.maps_state[state]][self.map_key[key]]