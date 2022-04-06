import yake


def extract_keywords(text):
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.1
    numOfKeywords = 5
    kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                         top=numOfKeywords, features=None)
    keywords = kw_extractor.extract_keywords(text)

    refined_keywords = [keyword[0] for keyword in keywords]

    text_list = []
    for extracted_text in refined_keywords:
        for segment in extracted_text.split(" "):
            text_list.append(segment)
    text_list = list(set(text_list))
    return text_list

