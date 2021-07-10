import re


def getDictionaryFromString(inputStringToConvert):
    myDict = {}
    strArr = inputStringToConvert.split(", ")
    convertedList = []
    for element in strArr:
        if element.strip():
            convertedList.append(element.strip())

    for element in convertedList:
        myList = element.split(":")
        if len(myList) > 1:
            if len(myList[1].split(",")) < 3:
                if (not "no" in myList[1].lower()) and (not "returnable" in myList[0].lower()):
                    myDict[myList[0]] = myList[1]
        else:
            myDict[element] = "Empty"

    return myDict


def removeSpecialChars(input):
    return re.sub('[^A-Za-z0-9]+', '', input)
