import csv

PATH_PARSING_TABLE = "./grammar/parsing_table.csv"

def get_parsing_table():
    """
    Read the parsing table from the csv file
    The first row is the keys
    The first column is the states
    The remaining cells are the parsing states
    Also turn the data in cells into int!!
    Returns:
        parseTable (2d list) : main parsing table
        states (dict) : map from state to int for table index access
        keys (dict) : map from key to int for table index access
    """
    
    data = list(csv.reader(open(PATH_PARSING_TABLE)))

    parseTable = []
    for i in range(1,len(data)):
        row = data[i][1:]
        parseTable.append(row)
        
    
    non_terminals = {data[i][0] : i-1 for i in range(1,len(data))}
    terminals = {data[0][i] : i-1 for i in range(1,len(data[0]))}
    return parseTable, non_terminals, terminals 

class Node:
    def __init__(self, val, type, children=None):
        self.val = val
        self.type = type
        self.children = children if children is not None else []

    # def __str__(self):
    #     return self.val
    
    def add_child(self, child):
        self.children.append(child)

class Tree:
    def __init__(self, inputs, start_state = "PROGRAM", end_state = "$"):
        self.i = 0
        self.inputs = inputs
        self.parseTable, self.non_terminals, self.terminals = get_parsing_table()
        self.start_state = start_state
        self.end_state = end_state
        self.root = self.build_tree(start_state)

    def get_current_input(self):
        x = self.inputs[self.i]
        if x not in self.terminals.keys():
            x = 'id'
        return x

    def transit(self, state, terminal) -> list:
        """
        Transition to the next state
        Change the state to the next state based on the terminals and nonterminals
        Args:
            state (str) : 
        Returns:
            
        """
        state = self.non_terminals[state]
        terminal = self.terminals[terminal]
        return self.parseTable[state][terminal]

    def print_tree(self, u):
        if u.type in self.terminals.keys():
            print('(', u.val, end=' ')
        for v in u.children:
            self.print_tree(v)
        print(')', end=' ')

    def build_tree(self, state):
        """
        Build a tree from inputs.
        Args:
            state: 
            inputs:
        Returns:
            node (Node) : the root of the tree
        """
        input = self.get_current_input()
        node = Node(input, state)
        print('State = ', state, '|Input = ', input)
        
        if state == input:
            self.i += 1
            return node

        if state == 'epsilon':
            return node
        
        if state not in self.non_terminals.keys():
            return node
        
        next_state_list = self.transit(state, input).split(' ')
        print('Next states = ', next_state_list)
        for next_state in next_state_list:
            if next_state == '':
                continue
            node.add_child(self.build_tree(next_state))
        return node