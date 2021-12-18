import re


def exportOptions(listKeywords, string):
    arrayString = string.split()
    options = []
    openBracketFlag = False
    for keyword in listKeywords:
        openBracketFlag = False
        for word in arrayString:
            if keyword + '"' in word:
                options.append("\n<" + re.sub(r'[0-9]', '', word[1:-2]) + ">\n")
                openBracketFlag = True
            elif openBracketFlag and ("]" == word or "]," == word):
                options.append("\n</" + re.sub(r'[0-9]', '', keyword) + ">")
                break;
            elif openBracketFlag:
                if "," == word or '",' in word:
                    options.append(word[:-1] + "\n")
                elif '[' == word or '{' == word or '}' == word:
                    continue
                elif '":' in word:
                    options.append(word[1:-2] + ":")
                else:
                    options.append(word)

    return (' '.join(options))


def saveOptions(listKeywords, string):
    arrayString = string.split()
    flagFirst = False
    options = []
    openBracketFlag = False
    for keyword in listKeywords:
        openBracketFlag = False
        for word in arrayString:
            if openBracketFlag and "]," == word:
                options.append("]")
                break;
            if '"' + keyword + '"' in word and flagFirst == True:
                options.append(",")
            if '"' + keyword + '"' in word or openBracketFlag:
                options.append(word)
                openBracketFlag = True
                flagFirst = True
            if openBracketFlag and "]" == word:
                break;
    return ("{" + ' '.join(options) + "}")
