import json
import pprint


def readFile(filename):
    file = open(filename, "r")
    return file.readlines()


def getpath(d, search_pattern, prev_datapoint_path=''):
    output = []
    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            if search_pattern in str(dkey):
                c = current_datapoint_path
                c += "['" + dkey + "']"
                output.append(c)
            c = current_datapoint_path
            c += "['" + dkey + "']"
            for i in getpath(current_datapoint[dkey], search_pattern, c):
                output.append(i)
    elif type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if search_pattern in str(i):
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(i)
            c = current_datapoint_path
            c += "[" + str(i) + "]"
            for i in getpath(current_datapoint[i], search_pattern, c):
                output.append(i)
    elif search_pattern in str(current_datapoint):
        c = current_datapoint_path
        output.append(c)
    output = filter(None, output)
    return list(output)


def saveOptions(listKeywords, string):
    arrayString = string.split()
    options = []
    openBracketFlag = False
    for keyword in listKeywords:
        openBracketFlag = False
        for word in arrayString:
            if keyword+'"' in word or openBracketFlag:
                options.append(word)
                openBracketFlag = True
            if openBracketFlag and "]" == word:
                break;
    return ("{"+''.join(options)+"}")
