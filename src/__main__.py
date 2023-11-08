from parser.automaton import Automaton

automaton = Automaton()

automaton.add_word('aapxj')
automaton.add_word('apaxj')
automaton.add_word('apaxf')
automaton.add_word('apagf')

print(automaton.root.prettify())

import pdb; pdb.set_trace()

# automaton.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt')
