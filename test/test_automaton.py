from mtac.automaton import ScrambledWordMatcher

def test_carry():
    automaton = ScrambledWordMatcher()

    automaton.add_word('abez')
    automaton.add_word('abfy')

    assert automaton.scan('aebz') == 1

def test_definition():
    automaton = ScrambledWordMatcher()

    automaton.add_word('axpaj')
    automaton.add_word('apxaj')
    automaton.add_word('dnrbt')
    automaton.add_word('pjxdn')
    automaton.add_word('abd')

    assert automaton.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt') == 4

def test_finish_on_carry():
    automaton = ScrambledWordMatcher()

    automaton.add_word('abeaz')
    automaton.add_word('abfy')

    assert automaton.scan('abeaz') == 1

def test_miss():
    automaton = ScrambledWordMatcher()

    automaton.add_word('abeaz')
    automaton.add_word('abfy')

    assert automaton.scan('abyf') == 0

def test_simple():
    automaton = ScrambledWordMatcher()

    automaton.add_word('star')
    automaton.add_word('loop')
    automaton.add_word('part')

    assert automaton.scan('wtsartsatroplopratlopostar') == 2
