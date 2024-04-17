import scanner.sm
from scanner.sm import StateMachine
from scanner.tokenizer import tokenize


def scan(token : str, debug = False) -> list:
    """
    Returns the terminal (final state) and kind of the token
    Using state machine to determine the kind of the token based on the transition table
    Args:
        token (str) : token
        debug (bool) : debug mode
    """

    sm = StateMachine()
    if debug:
        print(hex(id(sm.transTable)), "compare to", hex(id(StateMachine.transTable)))
    for c in token:
        if not sm.transition(c):
            if debug:
                print("ERROR in transition = .", token,"."," at c = ",ord(c),".",sep='')
            return -1, "ERROR"
    return sm.state, sm.getKind()

def scan_list(tokens: list) -> list:
    """
    Returns the list of info for each token
    Args:
        tokens (list str) : list of tokens
    """

    result = []
    for token in tokens:
        result.append(scan(token))
    return result


