import re
from itertools import islice
from nltk.stem.lancaster import LancasterStemmer

'''
def trimTitle(productTypeDict, titleProvided):
    for currentTitleContent in titleProvided.split():
        if currentTitleContent.strip() not in productTypeDict:
            titleProvided = titleProvided.replace(currentTitleContent, "")
    titleProvided = re.sub(' +', ' ', titleProvided)

    titleProvided = titleProvided.strip()
    wordArr = titleProvided.split()
    if len(wordArr) > 1:
        for w in wordArr:
            if len(w) == 1:
                titleProvided = titleProvided.replace(w, "")
        if len(titleProvided) > 0:
            return titleProvided
    else:
        return ""
'''


def trimTitle2(productTypeDict, titleProvided):
    constructed_sentence = ""
    primary_product_spec_values = set()
    primary_product_spec_keys = []
    secondary_product_spec_keys = []

    # print("Original Title: " + titleProvided)
    title = removeUnwantedWordFromOriginalTitle(titleProvided)
    # print("Removed Words Title: " + title)
    for w in title.split():
        primary_product_spec_values.add(w)

    for k in productTypeDict:
        if "product type" in k.lower():
            primary_product_spec_values.add(productTypeDict[k])
            primary_product_spec_keys.append(k)
        else:
            secondary_product_spec_keys.append(k)

    print(primary_product_spec_values)
    print("Secondary Keys: "+ str(secondary_product_spec_keys))
    constructed_sentence = constructed_sentence.join(" ").join(primary_product_spec_values)
    return constructed_sentence


def trimTitle(productTypeDict, titleProvided):
    listOfWords = []
    constructedSentence = ""

    for key in islice(productTypeDict, 4):
        listOfWords.append(key.split()[0])
        listOfWords.append(productTypeDict[key])

    print(listOfWords)

    constructedSentence = constructedSentence.join(" ").join(islice(listOfWords, 4))
    return constructedSentence


def removeUnwantedWordFromOriginalTitle(title):
    wordsArr = title.split()
    # only special characters
    regex = "[^a-zA-Z0-9]+"
    numberOnly = "[^a-zA-Z]+"
    # Compile the ReGex
    p = re.compile(regex)
    onlyNumbers = re.compile(numberOnly)

    for word in wordsArr:
        if re.search(p, word) or re.search(onlyNumbers, word) or len(word.strip()) <= 1:
            title = title.replace(word, "", 1)

    return title

'''
def removeUnwantedWordFromOriginalTitle(title):
    wordsArr = title.split()
    # only special characters
    regex = "[^a-zA-Z0-9]+"

    # Compile the ReGex
    p = re.compile(regex)

    for word in wordsArr:
        if re.search(p, word) or len(word.strip()) <= 1:
            title = title.replace(word, "", 1)

    return title
'''


def removeDuplicateWordsFromTitle(title):
    st = LancasterStemmer()
    s = title
    l = s.split()
    k = []
    singular_words = set()
    final_title_array = []
    consturcted_title =""
    for i in l:

        # If condition is used to store unique string
        # in another list 'k'
        if s.count(i) > 1 and (i not in k) or s.count(i) == 1:
            k.append(i)
    final_title =' '.join(k)
    for w in final_title.split():
        temp = st.stem(w)
        if temp not in singular_words:
            singular_words.add(temp)
            final_title_array.append(w)
    consturcted_title = consturcted_title.join(" ").join(final_title_array)
    return consturcted_title
    # return ' '.join(k)
