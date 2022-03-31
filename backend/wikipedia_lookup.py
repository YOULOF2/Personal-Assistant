import wikipedia


def wikipedia_search(text):
    return wikipedia.summary(text, sentences=3)

