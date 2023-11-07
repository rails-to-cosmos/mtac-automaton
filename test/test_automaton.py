from parser.automaton import Automaton

# def test_automaton_stores_sorted_representations():
#     automaton = Automaton()

#     automaton.add_word('aapxj')
#     automaton.add_word('apaxj')
#     automaton.add_word('apaxd')
#     automaton.add_word('apal')
#     automaton.add_word('apalc')
#     automaton.add_word('pda')
#     automaton.add_word('bpde')
#     automaton.add_word('bp')
#     automaton.add_word('bzd')
#     automaton.add_word('b')

#     print(' '.join(automaton.root.pretty()))

def test_automaton_factors():
    automaton = Automaton()
    automaton.add_word('axpaj')
    automaton.add_word('apxaj')
    assert automaton.root['a']['a']['p']['x']['j'].factor == 2
