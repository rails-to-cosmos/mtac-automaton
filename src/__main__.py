from parser.automaton import Automaton
from parser.data.tree import pretty

automaton = Automaton()

# automaton.add_word('aapxj')
# automaton.add_word('apaxj')
# automaton.add_word('apaxd')
# automaton.add_word('apal')
# automaton.add_word('apalc')
# automaton.add_word('pda')
# automaton.add_word('bpde')
# automaton.add_word('bp')
# automaton.add_word('bzd')
# automaton.add_word('b')

automaton.add_word('axpaj')
automaton.add_word('apxaj')
automaton.add_word('dnrbt')
automaton.add_word('pjxdn')
automaton.add_word('abd')

print(pretty(automaton.root))
