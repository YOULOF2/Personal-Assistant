from wiktionaryparser import WiktionaryParser

__all__ = ["dictionary_lookup"]


def dictionary_lookup(word):
    parser = WiktionaryParser()
    word = parser.fetch(word)
    definitions = word[0].get("definitions")[0].get("text")
    return definitions
