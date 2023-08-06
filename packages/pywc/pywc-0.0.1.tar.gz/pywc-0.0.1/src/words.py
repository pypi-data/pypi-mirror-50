from typing import Tuple
from collections import Counter

word_list = Tuple[str]

def get_words(string: str) -> word_list:
    '''
    Provides a list of words in the string.
    Returns a tuple of words
    string - A sentence or phrase from which to extract words.
    Assumes that only one sentence is given as input.
    '''
    import re
    string = re.sub(r"[෴۔።।.?!؟]+", "", string) # remove sentence enders from words
    words = re.split(r'[​          ⠀\t]', string) # unicode whitespace charcters
    return Counter(filter(lambda _: len(_) > 0, words))

def count_words(string: str) -> int:
    '''
    Counts the number of words in a sentence / phrase
    Returns the total number of words in the string.
    string - A sentence or phrase from which to count the words
    '''
    return len(get_words(string))
