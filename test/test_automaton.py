from mtac.automaton import Automaton

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

#     print(' '.join(automaton.root.prettify()))

def test_automaton_weights():
    automaton = Automaton()
    automaton.add_word('axpaj')
    automaton.add_word('apxaj')
    assert automaton.root['a']['a']['p']['x']['j'].weight == 2

def test_carry():
    automaton = Automaton()

    automaton.add_word('abez')
    automaton.add_word('abfy')

    assert automaton.scan('aebz') == 1

def test_definition():
    automaton = Automaton()

    automaton.add_word('axpaj')
    automaton.add_word('apxaj')
    automaton.add_word('dnrbt')
    automaton.add_word('pjxdn')
    automaton.add_word('abd')

    assert automaton.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt') == 4

# def test_finish_on_carry():
#     automaton = Automaton()

#     automaton.add_word('abeaz')
#     automaton.add_word('abfy')

#     print(automaton.root.prettify())
#     assert automaton.scan('abeaz') == 1

# def test_finish_on_carry_2():
#     automaton = Automaton()

#     automaton.add_word('abeaz')
#     automaton.add_word('abfy')

#     print(automaton.root.prettify())
#     assert automaton.scan('abyf') == 1
