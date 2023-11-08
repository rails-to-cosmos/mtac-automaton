from matcher import ScrambledWordMatcher

def test_carry():
    matcher = ScrambledWordMatcher()

    matcher.add_word('abez')
    matcher.add_word('abfy')

    assert matcher.scan('aebz') == 1

def test_definition():
    matcher = ScrambledWordMatcher()

    matcher.add_word('axpaj')
    matcher.add_word('apxaj')
    matcher.add_word('dnrbt')
    matcher.add_word('pjxdn')
    matcher.add_word('abd')

    assert matcher.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt') == 4

def test_finish_on_carry():
    matcher = ScrambledWordMatcher()

    matcher.add_word('abeaz')
    matcher.add_word('abfy')

    assert matcher.scan('abeaz') == 1

def test_miss():
    matcher = ScrambledWordMatcher()

    matcher.add_word('abeaz')
    matcher.add_word('abfy')

    assert matcher.scan('abyf') == 0

def test_simple():
    matcher = ScrambledWordMatcher()

    matcher.add_word('star')
    matcher.add_word('loop')
    matcher.add_word('part')

    assert matcher.scan('wtsartsatroplopratlopostar') == 2

def test_multi_scan():
    matcher = ScrambledWordMatcher()

    matcher.add_word('axpaj')
    matcher.add_word('apxaj')
    matcher.add_word('dnrbt')
    matcher.add_word('pjxdn')
    matcher.add_word('abd')

    assert matcher.scan('aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt') == 4
    assert matcher.scan('aapxj') == 2
    assert matcher.scan('adb') == 0
    assert matcher.scan('adbtpdxjn') == 1
