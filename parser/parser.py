from parser import tree

def parse(tokens, kinds, lines, start_state = "PROGRAM", end_state = "$"):
    
    # Build the parseTree and compress the tree
    parseTree = tree.Tree(tokens, kinds, lines, start_state, end_state)
    parseTree.node_compress(parseTree.root)
    
    # Get the parsed lines from the parseTree
    parseTree.get_parsed_in_lines(parseTree.root)
    str_list = parseTree.str_buffer
    
    # Remove blank lines, trim spaces
    for str in str_list:
        str = str.strip()
        if str == '':
            str_list.remove(str)
    return str_list

