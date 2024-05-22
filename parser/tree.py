import csv

PATH_PARSING_TABLE = "./grammar/parsing_table.csv"
PATH_TERMINALS = 'graph/terminals.csv'
EXPR_LIST = [
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
    def __init__(self, val, type, line = 0, children=None):
        self.val = val
        self.type = type
        self.line = line
        self.children = children if children is not None else []

    # def __str__(self):
    #     return self.val
    
    def add_child(self, child):
        if child is not None:
            self.children.append(child)

    def print(self, tree_str=''):
        if self.children == []:
            tree_str += self.val + ' '
        elif self.type in SUB_EXPR_LIST:
            if len(self.children) == 3:
                tree_str = '(' + tree_str + self.children[0].print(str(tree_str)) + self.children[1].print(str(tree_str)) + ')' + self.children[2].print(str(tree_str))
            if len(self.children) == 2:
                tree_str = '(' + tree_str + self.children[0].print(str(tree_str)) + self.children[1].print(str(tree_str)) + ')'
        elif self.type in EXPR_LIST:
            if len(self.children) == 1:
                tree_str = tree_str + self.children[0].print(str(tree_str))
            else:
                for child in self.children:
                    tree_str = tree_str + child.print(str(tree_str))
        else: 
            # print(self.val, end=' ')
            for child in self.children:
                tree_str = tree_str + child.print(str(tree_str))
        return tree_str
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
        self.cur_line = 0

    def build_tree(self, state):
        if state == '' or state == 'epsilon':
            return None
        
        input, type, line  = self.get_current_input()
        if input == self.end_state:
            return None
        node = Node(input, state, line)
        # print('Input = ', input, '| State = ', state)
        
        if state == type:
            self.i += 1
            return node

        next_state_list = self.transit(state, type).split(' ')
        # print('Next states = ', next_state_list)
        for next_state in next_state_list:
            v = self.build_tree(next_state)
            if v is not None:
                node.add_child(v)

        return node

    def get_current_input(self):
        return self.tokens[self.i], self.kinds[self.i], self.lines[self.i]

    def transit(self, state, type) -> list:
        state = self.non_terminals[state]
        # if terminal not in self.terminals.keys():
        #     terminal = 'id'
        type = self.terminals[type]
        return self.parseTable[state][type]

    def node_compress(self, u):
        # if u.children == []:
        #     return u if u.type != 'epsilon' else None
        new_children = []
        for v in u.children:
            new_v = self.node_compress(v)
            if new_v is not None:
                new_children.append(new_v)
        if len(new_children) == 0:
            return u if u.type in self.terminals else None
        if len(new_children) == 1:
            return new_children[0]
        u.children = new_children
        return u

    def print_tree(self, u, spaces=0):
        _spaces = ' '*spaces
        print(f'{_spaces}|{u.val}|', u.type, 'num child =', len(u.children))
        if u.children == []:
            print('=======================')
        for v in u.children:
            self.print_tree(v, spaces+2)

    def print_parsed(self, u):
        if u.type in self.terminals.keys() and u.type != 'epsilon':
            print('(', end=' ')
        if u.type in self.terminals.keys():
            print(u.val, end=' ')
        for v in u.children:
            self.print_parsed(v)
        if u.type in self.terminals.keys() and u.type != 'epsilon':
            print(')', end=' ')
    
    def print_parsed_in_lines(self, u, next_endl = False):
        if self.cur_line < u.line:
            print()
            self.cur_line = u.line
        if u.type in EXPR_LIST:
            print('(', end=' ')
        if u.type in self.terminals.keys():
            print(u.val, end=' ')
        elif next_endl: # and u.type in SUB_EXPR_LIST:
            print(')', end=' ')
        for v in u.children:
            self.print_parsed_in_lines(v, next_endl or u.type in EXPR_LIST)
        if u.type in EXPR_LIST:
            print(')', end=' ')