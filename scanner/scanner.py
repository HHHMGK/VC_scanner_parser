from scanner.sm import StateMachine
from scanner.tokenizer import tokenizer

def state_kind(token: str) -> str:
    # Returns the kind of the token
    sm = StateMachine()
    for c in token:
        if not sm.transition(c):
            return "ERROR"
    return sm.state, sm.getKind()

def scan(token : str) -> list:
    # Returns the info(s) for the token
    state, kind = state_kind(token)
    return [token, state, kind]

def scan_tokens(tokens: list) -> list:
    # Returns the list of info for each token
    result = []
    for tok in tokens:
        result.append(scan(tok))
    return result

def scan_file(text: str) -> list:
    # Returns the list of info for each token
    tokens = tokenizer(text)
    return scan_tokens(tokens)

