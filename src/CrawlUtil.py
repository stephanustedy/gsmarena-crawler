__author__ = 'Natan Elia'

import requests
import json

def cls():
    print(chr(27) + "[2J")

def cll():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

def postJSON(targeturl, data):
    s = requests.Session()
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))

    r = s.post(targeturl, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return r.json()

def getJSON(s, targeturl):
    r = s.get(targeturl)

    nret = 2
    if r.text.startswith('<!DOCTYPE', 0, 10) and nret > 0:
        nret -= 1
        return getJSON(s, targeturl)

    try:
        return r.json()
    except ValueError:
        print("Error retrieving json: ", targeturl)
        print(r.text)
        sys.exit()
