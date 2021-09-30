import re


def identifyOptionKeywords(string):
    arrayString = string.split()
    arrayOptionKeywords = []
    for word in arrayString:
        if ("custom_item" in word)  or ('"item' in word):
            arrayOptionKeywords.append(word[1:-2])
    return (arrayOptionKeywords)


def mainParse(readFilename):
    keywords = []
    prevKeyword = ""
    lineNotEnded = False
    closingBracket = False
    openBracketPrev = False
    countKeys = 0

    openFile = readFilename

    def readFile(filename):
        file = open(filename, "r")
        return file.readlines()

    def writeFile(filename):
        writeNewFile = open(filename, "w")
        writeNewFile.write("")
        writeNewFile.close()
        return open(filename, "a")

    def verifyPreviousLine(prevKeyword, line, tempKeyword, countKeys):
        newTempKeyword = tempKeyword + str(countKeys)
        if len(keywords) > 0:
            if closingBracket:
                parsedFile.write("," + '"' + newTempKeyword + '"' + ":[{")
            else:
                parsedFile.write('"' + newTempKeyword + '"' + ":[{")
        else:
            parsedFile.write('"' + newTempKeyword + '"' + ":[{")
        return countKeys + 1

    def printValues(line):
        lineParts = line.partition(":")
        parsedFile.write('"' + lineParts[0].strip() + '"' + ":")
        rightSide = lineParts[2].strip()
        newRightSide = re.sub("([^\\\\])\\\\([^\\\\\"\'])", '\\1\\\\\\\\\\2', rightSide)
        newRightSide = newRightSide.replace("\\'", "\\\\'")
        if line.count('" || "') > 0:
            parsedFile.write('"' + newRightSide.replace('"', '\\"') + '"')
        elif (rightSide[0] != '"'):
            parsedFile.write('"' + newRightSide + '"')
        else:
            parsedFile.write(newRightSide)
        if (rightSide[- 1] != '"'):
            if (rightSide[0] == '"'):
                return True
        return False

    def cutKeyword(stripLine, symbol):
        return stripLine[stripLine.find("<") + len("<"):stripLine.find(symbol)]

    lines = readFile(openFile)
    parsedFile = writeFile(readFilename.split(".audit")[0] + ".json")

    parsedFile.write("{")

    for line in lines:

        stripLine = line.strip()
        if stripLine == "" or (not lineNotEnded and stripLine[0] == '#'):
            continue
        openingBracket = bool(re.search("^<[^/].+>", stripLine))
        closingBracketLine = bool(re.search("(</.+>)", stripLine))
        if (not closingBracketLine and not openingBracket) or lineNotEnded:
            if (not lineNotEnded):
                if not openBracketPrev and not closingBracket:
                    parsedFile.write(",")
                lineNotEnded = printValues(line)
            else:
                newRightSide = re.sub("([^\\\\])\\\\([^\\\\\"\'])", '\\1\\\\\\\\\\2', stripLine)
                parsedFile.write(newRightSide)
                if stripLine[- 1] == '"':
                    lineNotEnded = False
            openBracketPrev = False
            # for case when brackets are on diff lines
        else:
            if closingBracketLine:
                closingBracket = True
                parsedFile.write("}")
                parsedFile.write("]")
                prevKeyword = keywords.pop()
                openBracketPrev = False
            elif openingBracket:
                if " " in stripLine:
                    tempKeyword = cutKeyword(stripLine, " ")
                elif "_" in stripLine and ":" in stripLine:
                    tempKeyword = cutKeyword(stripLine, "_")
                else:
                    tempKeyword = cutKeyword(stripLine, ">")
                countKeys = verifyPreviousLine(prevKeyword, line, tempKeyword, countKeys)
                closingBracket = False
                keywords.append(tempKeyword)
                openBracketPrev = True
    parsedFile.write("}")
    parsedFile.close()
