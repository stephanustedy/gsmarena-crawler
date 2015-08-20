__author__ = 'Natan Elia'

from os import walk
import sys
import re
import json
import time
from pprint import pprint

def printErr(err):
    print("[ERROR] " + err)

def printProcess(process):
    print("[PROCESS] " + process)

def listFiles(path, scanParentOnly=False):
    f = []
    d = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        d.extend(dirnames)
        if scanParentOnly:
            break

    return (f, d)

def readJSONFile(fileName):
    with open(fileName, "r") as fileData:
        data = fileData.read()
    return json.loads(data)

def readJSONFiles(path, fileNames):
    d = []
    for (fileName) in fileNames:
        fileName = path + "/" + fileName
        sp = fileName.split(".")
        if len(sp) > 1 and sp[len(sp) - 1] == 'json':
            d.append(readJSONFile(fileName))
    return d

def returnEmptyIfNone(dataMap, *keys):
    try:
        if len(keys) == 1:
            return dataMap[''.join(keys[0])]
        else:
            dataMap = dataMap[keys[0]]
            return returnEmptyIfNone(dataMap, keys[1:])
    except KeyError:
        return ''

def removeInsideParentheses(str):
    return re.sub(r'(\s+)*\(.+\)', '', str)

def getSize(str):
    if str == '-' or str == '': return ('','','')
    size = removeInsideParentheses(str)

    if ' ' not in size: return ('','','')
    sizes = size.split(' ')
    unit = sizes[len(sizes) - 1]
    height = sizes[0] + ' ' + unit

    if len(sizes) <= 2: return ('','','')
    width = sizes[2] + ' ' + unit

    if len(sizes) <= 4: return (height, width, '')
    thickness = sizes[4] + ' ' + unit
    return (height, width, thickness)

def mapToCSVLine(indexMap, dataMap):
    result = []
    for colName in indexMap:
        result.append(dataMap[colName])
    # print(re.sub(r'[^\x00-\x7F]+',' ', '","'.join(result)))
    return '"' + '","'.join(result) + '"'

def getCurrentDate():
    return (time.strftime("%d/%m/%Y"))

def sanitizeString(str):
    return re.sub(r'[^A-Za-z0-9. ]*', '', re.sub(r'\-', ' ', str))

def sanitizeStringWithSpace(str):
    return re.sub(r'[^A-Za-z0-9. ]+', ' ', str)