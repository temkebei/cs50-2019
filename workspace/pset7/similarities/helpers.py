from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    # split strings to lines then to sets (no duplicate elements)
    aLines = set(a.split("\n"))
    bLines = set(b.split("\n"))

    # return elements in both a & b
    return aLines & bLines


def sentences(a, b):
    """Return sentences in both a and b"""
    # split strings to sentences then to sets (no duplicate elements)
    aSentences = set(sent_tokenize(a))
    bSentences = set(sent_tokenize(b))

    # return elements in both a & b
    return aSentences & bSentences


def substr(str, n):
    substrings = []

    # calculate the possibilities
    for i in range(len(str) - n + 1):
        # slice the string from current position (i) to (i + n) position
        substrings.append(str[i:i + n])

    return substrings


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # slice strings with our substr function then put the lists to sets (no duplicate elements)
    aSubstrings = set(substr(a, n))
    bSubstrings = set(substr(b, n))

    # return elements in both a & b
    return aSubstrings & bSubstrings