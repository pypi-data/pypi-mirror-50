from collections import Counter

def get_sentences(string):
    import re
    string = string.replace("\n", "") # remove newline because we will be dividing by newline later
    sentence_delimiters = r"([෴۔።।.?!؟]+) *"
    string = re.sub(sentence_delimiters, r"\1\n", string)
    string = string.split("\n")
    return Counter(filter(lambda _: len(_) > 0, string))
