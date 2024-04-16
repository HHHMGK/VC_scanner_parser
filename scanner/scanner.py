import scanner.sm
from scanner.sm import StateMachine
from scanner.tokenizer import tokenize\

def terminal_kind(token: str) -> str:
    # Returns the terminal (final state) and kind of the token
    # Using state machine to determine the kind of the token based on the transition table
    
    sm = StateMachine()
    for c in token:
        if not sm.transition(c):
            print("ERROR in transition = .", token,"."," at c = ",ord(c),".",sep='')
            return -1, "ERROR"
    return sm.state, sm.getKind()

def scan(token : str) -> list:
    # Returns the info(s) for the token
    state, kind = terminal_kind(token)
    return (token, state, kind)

def scan_list(tokens: list) -> list:
    # Returns the list of info for each token
    result = []
    for token in tokens:
        result.append(terminal_kind(token))
    return result


