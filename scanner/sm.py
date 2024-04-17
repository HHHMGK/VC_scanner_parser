import csv

PATH_TRANSITION_TABLE = "./graph/transition_table.csv"
PATH_TERMINALS = "./graph/terminals.csv"

def get_transition_table():
    """
    Read the transition table from the csv file
    The first row is the keys
    The first column is the states
    The remaining cells are the transition states
    Also turn the data in cells into int!!
    Returns:
        transTable (2d list) : main transition table
        states (dict) : map from state to int for table index access
        keys (dict) : map from key to int for table index access
    """
    
    data = list(csv.reader(open(PATH_TRANSITION_TABLE)))

    transTable = []
    for i in range(1,len(data)):
        row = data[i][1:]
        for j in range(len(row)):
            if row[j] != '':
                row[j] = int(row[j])
        transTable.append(row)
        
    # Map the state to int for table index access
    # = i-1 because the first row is the states and the transTable is 0-indexed
    states = {}
    for i in range(1,len(data)):
        states[int(data[i][0])] = i-1

    # Map the key to int for table index access
    keys = {}
    for i in range(1,len(data[0])):
        keys[data[0][i]] = i-1

    # csv.writer(open("test.csv","w+",newline='')).writerows(transTable)
    return transTable, states, keys

def get_terminals(states : dict):
    """
    Read the terminals from the csv file
    The first column is the terminal states
    The second column is the kind of the token
    Args:
        states (dict) : map from state to int for table index access
    Returns:
        terminals (dict) : map from state to the kind of the token
    """
    
    data = list(csv.reader(open(PATH_TERMINALS)))

    # Get all the terminals
    terminals = {}
    for i in range(1,len(data)):
        terminals[states[int(data[i][0])]] = data[i][1]

    return terminals

class StateMachine:
    # Common variables for all instances of the class
    transTable, states, keys = get_transition_table()
    terminals = get_terminals(states)
    
    def __init__(self):
        # Initial state
        self.state = 0
    
    def transit(self, key) -> bool:
        """
        Transition to the next state
        Change the state to the next state based on the key and the transition table
        Using the keys and states to map to table index
        Args:
            key (str) : key to transit from the current state
        Returns:
            bool : True if the transition is successful, False otherwise
        """
        if key not in StateMachine.keys:
            return False
        
        key = StateMachine.keys[key]
        if StateMachine.transTable[self.state][key] == '':
            return False
        self.state = StateMachine.transTable[self.state][key]
        self.state = StateMachine.states[self.state]
        return True

    def getKind(self):
        """
        Return the kind of the token based on the current state - final state of the token
        Returns:
            str : kind of the token
        """
        if self.state not in StateMachine.terminals:
            return "ERROR_STATE_NOT_TERMINAL"
        return StateMachine.terminals[self.state]
        