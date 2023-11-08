from mtac.automaton import ScrambledWordMatcher

automaton = ScrambledWordMatcher()

# automaton = ScrambledWordMatcher()

# automaton.add_word('aapxj')
# automaton.add_word('apaxj')
# automaton.add_word('apaxf')
# automaton.add_word('apagf')
# automaton.add_word('apa')

# print(automaton.root.prettify())

# automaton.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt')

# automaton = ScrambledWordMatcher()

# automaton.add_word('abez')
# automaton.add_word('abfy')

# print(automaton.root.prettify())

# automaton.scan('aebz')

# print(automaton.root.prettify())
# automaton.scan('afby')
# print(automaton.root.prettify())

# automaton.add_word('axpaj')
# automaton.add_word('apxaj')
# automaton.add_word('dnrbt')
# automaton.add_word('pjxdn')
# automaton.add_word('abd')

# print(automaton.root.prettify())
# automaton.scan('aapxjdnrbt')
# print(automaton.root.prettify())

# automaton.add_word('axpaj')
# automaton.add_word('apxaj')
# automaton.add_word('dnrbt')
# automaton.add_word('pjxdn')
# automaton.add_word('abd')

# automaton.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt')

automaton.add_word('star')
automaton.add_word('loop')
automaton.add_word('part')
automaton.scan('wtsartsatroplopratlopostar')
# print(automaton.root.prettify())
#
# print(automaton.root.prettify())
