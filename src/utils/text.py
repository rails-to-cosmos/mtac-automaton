import functools as ft


@ft.cache
def normalize_word(word: str) -> str:
    """
    Normalizes a word by rearranging its inner characters in alphabetical order,
    while keeping the first and last characters in place.

    Parameters:
    word (str): The word to be normalized.

    Returns:
    str: The normalized word.

    If the input word has a length of 3 or less, it remains unchanged.
    For longer words, the first and last characters are preserved, and the
    inner characters are sorted in alphabetical order.

    Examples:
    >>> normalize_word("apple")
    'alppe'

    >>> normalize_word("python")
    'photyn'

    >>> normalize_word("cat")
    'cat'

    >>> normalize_word("ab")
    'ab'

    >>> normalize_word("xyz")
    'xyz'
    """

    if len(word) <= 3:
        return word

    return word[0] + ''.join(sorted(word[1:len(word) - 1])) + word[-1]
