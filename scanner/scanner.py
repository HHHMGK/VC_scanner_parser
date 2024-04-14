import scanner.sm
from scanner.sm import StateMachine
from scanner.tokenizer import tokenizer

def state_kind(token: str) -> str:
    # Returns the kind of the token
    sm = StateMachine()
    print(token)
    for c in token:
        if not sm.transition(c):
            return -1, "ERROR"
    return sm.state, sm.getKind()

def scan(token : str) -> list:
    # Returns the info(s) for the token
    state, kind = state_kind(token)
    return (token, state, kind)

def scan_tokens(tokens: list) -> list:
    # Returns the list of info for each token
    result = []
    for token in tokens:
        result.append(state_kind(token))
    return result


