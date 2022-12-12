from rutermextract import TermExtractor
# import asyncio


def key_words(text):
    term_extractor = TermExtractor()
    # print(term_extractor(text))
    word_list = []
    for term in term_extractor(text):
        word_list.append(term.normalized)
        print(term.normalized)
    # for w in word_list:
    #     print(w)

    return word_list
    # chanels_def(word_list)
    # for w in word_list:
    #     print(w)
