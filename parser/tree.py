import csv

PATH_PARSING_TABLE = "./grammar/parsing_table.csv"
EXPR_LIST = [
    'EXPR',
    'ASSIGNMENT_EXPR',
    'CONDITION_OR_EXPR',
    'CONDITION_AND_EXPR',
    'EQUALITY_EXPR',
    'RELATIONAL_EXPR',
    'ADDITIVE_EXPR',
    'MULTIPLICATIVE_EXPR',
    'UNARY_EXPR'
]
SUB_EXPR_LIST = [
    'ASSIGNMENT_EXPR_1',
    'CONDITION_OR_EXPR_1',
    'CONDITION_AND_EXPR_1',
    'EQUALITY_EXPR_1',
    'RELATIONAL_EXPR_1',
    'ADDITIVE_EXPR_1',
    'MULTIPLICATIVE_EXPR_1',
    'UNARY_EXPR_1'
]

def get_parsing_table():
    """
    Read the parsing table from the csv file
    The first row is the terminals
    The first column is the non terminals
    The remaining cells are the parsing states
    Returns:
        parseTable (2d list) : main parsing table
        non_terminals (dict) : non terminals (str : row index)
        terminals (dict) : terminals (str : column index)
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
    def __init__(self, val, state, line = 0, children=None):
        self.val = val
        self.state = state
        self.line = line
        self.children = children if children is not None else []
        self.num_sub = 0

    # def __str__(self):
    #     return self.val
    
    def add_child(self, child):
        if child is None:
            return
        self.children.append(child)
        if child.state in SUB_EXPR_LIST:
            self.num_sub += child.num_sub + 1

class Tree:
    def __init__(self, tokens, kinds, lines, start_state = "PROGRAM", end_state = "$"):
        self.i = 0
        self.tokens = tokens
        self.kinds = kinds
        self.lines = lines
        self.parseTable, self.non_terminals, self.terminals = get_parsing_table()
        self.start_state = start_state
        self.end_state = end_state
        self.root = self.build_tree(start_state)
        self.str_buffer = ['' for _ in range(max(lines)+1)]

    def get_current_input(self):
        """
        Get the current input in form of (token, kind, line) by the index i
        """
        return self.tokens[self.i], self.kinds[self.i], self.lines[self.i]

    def transit(self, state, type) -> list:
        """
        Get the next state(s) from the current state and input type in list form
        """
        if state not in self.non_terminals.keys():
            print('Invalid state ', state)
            return []
        if type not in self.terminals.keys():
            print('Invalid type ', type)
            return []
        state = self.non_terminals[state]
        type = self.terminals[type]
        return self.parseTable[state][type].split(' ')
    
    def build_tree(self, state):
        """
        Build the (sub)tree from the current state
        Returns the root node of the tree
        """
        if state == '' or state == 'epsilon':
            return None
        
        raw_input, input_type, line  = self.get_current_input()
        if raw_input == self.end_state:
            return None 
        node = Node(raw_input, state, line)
        # print('Input = ', input, '| State = ', state)
        
        if state == input_type:
            self.i += 1
            return node

        # print('State =', state, raw_input, input_type)
        next_state_list = self.transit(state, input_type)
        # print('Next state =', next_state_list)
        for next_state in next_state_list:
            v = self.build_tree(next_state)
            if v is not None:
                node.add_child(v)

        return node


    def node_compress(self, u):
        """
        Compress the node u by removing the unnecessary nodes
        Returns the new node u
        """
        # Recursively compress the children first
        new_children = []
        for v in u.children:
            new_v = self.node_compress(v)
            if new_v is not None:
                new_children.append(new_v)
        # If the node u is a terminal, return the node u itself
        if len(new_children) == 0:
            return u if u.state in self.terminals else None
        # If the node u has only one child, return the child i.e compress the node u
        if len(new_children) == 1:
            return new_children[0]
        u.children = new_children
        return u        

    def print_tree(self, u, spaces=0):
        """
        Print the tree from the node u, with the indentation of spaces as the node level
        """
        _spaces = ' '*spaces
        print(f'{_spaces}|{u.val}|', u.state, 'num child =', len(u.children))
        if u.children == []:
            print('=======================')
        for v in u.children:
            self.print_tree(v, spaces+2)

    def get_parsed_in_lines(self, u):
        """
        Get the parsed form of input souce code in lines of string
        """
        # Print the node if it is a terminal
        if u.state in self.terminals.keys():
            self.str_buffer[u.line] += u.val + ' '
            return
        
        # Print the children of the node
        # EXPR nodes have 2 children of the form (id, expr)
        if u.state in EXPR_LIST:
            self.str_buffer[u.line] += '('*(u.num_sub-1) + ' '
            self.get_parsed_in_lines(u.children[0])
            self.get_parsed_in_lines(u.children[1])
        # SUB_EXPR nodes have children of the form (expr, operator, expr) or (operator, expr)
        elif u.state in SUB_EXPR_LIST:
            self.get_parsed_in_lines(u.children[0])
            self.get_parsed_in_lines(u.children[1])
            self.str_buffer[u.line] += ') '
            if len(u.children) == 3:
                self.get_parsed_in_lines(u.children[2])
        # Recursively print the children
        else:
            for v in u.children:
                self.get_parsed_in_lines(v)