import csv

def get_transition_table():
    # Read the transition table
    data = list(csv.reader(open("./graph/transition_table.csv")))
    # The first row is the keys
    # The first column is the states
    # The remaining cells are the transition states
    # Also turn the data in cells into int!!

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
    # Read the terminals
    # Using the states dict to map from state for transTable index access
    data = list(csv.reader(open("./graph/terminals.csv")))

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
    
    def transition(self, key) -> bool:
        # Transition to the next state
        # Returns False there's no matching transition key from the state
        if key not in StateMachine.keys:
            return False
        
        key = StateMachine.keys[key]
        if StateMachine.transTable[self.state][key] == '':
            return False
        self.state = StateMachine.transTable[self.state][key]
        self.state = StateMachine.states[self.state]
        # print(self.state, type(self.state))
        return True

    def getKind(self):
        # Returns the kind of the token after reaching terminal state
        if self.state not in StateMachine.terminals:
            return "ERROR_STATE_NOT_TERMINAL"
        return StateMachine.terminals[self.state]
        