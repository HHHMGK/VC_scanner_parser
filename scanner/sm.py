# STATE MACHINE

from typing import Any


class StateMachine:
    # Common variables for all instances of the class
    transTable = []
    terminals = []

    def __init__(self):
        # Initial state
        self.state = 0
    
    def transition(self, key) -> bool:
        # Transition to the next state
        # Returns False there's no matching transition key from the state
        if StateMachine.transTable[self.state][key] == '':
            return False
        self.state = StateMachine.transTable[self.state][key]
        return True
        

    def getKind(self) -> Any:
        # Returns the kind of the token after reaching terminal state
        if self.state not in StateMachine.terminals:
            return [-1,"ERROR_STATE_NOT_TERMINAL"]
        return [self.state, StateMachine.terminals[self.state]]
        