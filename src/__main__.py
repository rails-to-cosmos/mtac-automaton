from src.automaton import Automaton

if __name__ == '__main__':

    automaton = Automaton()
    automaton.add_word('aapxj')
    automaton.add_word('apaxj')
    automaton.add_word('apaxd')
    automaton.add_word('apal')
    automaton.add_word('pda')
    automaton.add_word('bpd')
    automaton.add_word('bp')
    automaton.add_word('bzd')
    automaton.add_word('b')

    print(' '.join(automaton.root.pretty()))
