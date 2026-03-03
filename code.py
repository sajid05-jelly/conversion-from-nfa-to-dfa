from collections import defaultdict, deque

class NFA:
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.start_state = None
        self.final_states = set()
        self.states = set()
        self.alphabet = set()

    def add_transition(self, from_state, symbol, to_state):
        self.transitions[from_state][symbol].add(to_state)
        self.states.update([from_state, to_state])
        if symbol != 'ε':
            self.alphabet.add(symbol)

    def set_start(self, state):
        self.start_state = state
        self.states.add(state)

    def add_final(self, state):
        self.final_states.add(state)
        self.states.add(state)

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            for next_state in self.transitions[state]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure


def nfa_to_dfa(nfa):
    dfa_transitions = {}
    dfa_final_states = set()

    start_closure = frozenset(nfa.epsilon_closure({nfa.start_state}))
    queue = deque([start_closure])
    visited = set([start_closure])

    while queue:
        current = queue.popleft()
        dfa_transitions[current] = {}

        for symbol in nfa.alphabet:
            next_states = set()

            for state in current:
                next_states |= nfa.transitions[state][symbol]

            next_closure = frozenset(nfa.epsilon_closure(next_states))

            if next_closure:
                dfa_transitions[current][symbol] = next_closure

                if next_closure not in visited:
                    visited.add(next_closure)
                    queue.append(next_closure)

    for state in visited:
        if any(s in nfa.final_states for s in state):
            dfa_final_states.add(state)

    return dfa_transitions, start_closure, dfa_final_states
