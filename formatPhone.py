#!/usr/bin/env python3

__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath('src'))

import Phone
import Util
import time

def main(argv):
    if (len(argv) <= 0):
        Util.printErr("You have not specified any dirpath.")
        Util.printErr("Write something like this: new.py dirpath [scanParentOnly? True|False]")
        return

    if (len(argv) > 1):
        scanParentOnly = argv[1]
    else:
        scanParentOnly = False

    dirToScan = argv[0]
    (f, d) = Util.listFiles(dirToScan, scanParentOnly)

    Util.printProcess('Reading JSONs')
    jsons = Util.readJSONFiles(dirToScan, f)
    print(len(jsons), 'files read.')

    fileOut = input('Save CSV filename: ')
    Util.printProcess('Converting to single CSV...')

    startTime = time.time()
    indexMap = Phone.createPhoneIndexMap()
    Phone.mapToCSV(jsons, indexMap, fileOut + '.csv')
    print('Success! {:f} secs'.format(time.time() - startTime))

main(sys.argv[1:])