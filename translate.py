from googletrans import Translator, constants
# from keyWords import key_words

from pprint import pprint

def translate_phrase(text):
    translator = Translator()
    # print(text)

    try:
        translation = translator.translate(text, dest="ru")
    except:
        print("Error")

    if translation.src == "uk":
        translation = translator.translate(text, src="uk", dest="ru")
        # print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    elif translation.src == "ru":
        translation = translator.translate(text, src="ru", dest="uk")
        # print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

    return translation.src, translation.text

# init the Google API translator
#     translator = Translator()
#
#     if translator.translate(src="uk") == True:
#
#
# # translate a spanish text to arabic for instance
#     translation = translator.translate(text, src="uk", dest="ru")
#     # print("here")
#     # key_words(translation.text)
#     return translation.text
    #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

