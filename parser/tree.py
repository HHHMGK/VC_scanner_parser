import parseTable

class Node:
    def __init__(self, val, children=None):
        self.value = val
        self.children = children if children else []

    def __str__(self):
        return self.value
    
    def add_child(self, child):
        self.children.append(child)

def build_tree(i, tokens):
    """
    Build a tree from a list of tokens.
    Args:
        i (int) : index of the current token
        tokens (list) : list of tokens
    Returns:
        node (Node) : the root of the tree
    """
    state = tokens[i]
    node = Node(state)
    next_states = parseTable.transit(state, tokens[i])
    