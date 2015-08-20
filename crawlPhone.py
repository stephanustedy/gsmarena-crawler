#!/usr/bin/env python3

__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath('src'))

import CrawlUtil
import json
import requests
import time
import threading
from queue import Queue
from pprint import pprint

def processPhone(phoneUrl, num, numTotal):
    startTime = time.time()

    s = requests.Session()
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))

    phoneAPIUrl = "https://www.kimonolabs.com/api/7ltn7gno?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN&kimmodify=1"
    
    resp = CrawlUtil.postJSON('https://ws.kimonolabs.com/ws/updateapi/', {'apiid': '7ltn7gno', 'updateObj': {'targeturl' : phoneUrl}})
    if resp['success']:
        resp = CrawlUtil.postJSON('https://ws.kimonolabs.com/ws/startcrawl/', {'apiid': '7ltn7gno'})
        if resp['success']:
            resp = CrawlUtil.getJSON(s, 'https://ws.kimonolabs.com/ws/crawlstats/?apiid=7ltn7gno')
            while (resp['isCrawling'] != False):
                var = None
                resp = CrawlUtil.getJSON(s, 'https://ws.kimonolabs.com/ws/crawlstats/?apiid=7ltn7gno')

            phoneJson = CrawlUtil.getJSON(s, phoneAPIUrl)
            phoneResult = phoneJson['results']

            deviceName = phoneResult['main']['device_name']

            if not os.path.exists('results'):
                os.makedirs('results')

            f = open('phones/' + deviceName.replace("/", "-", 100) + '.json', 'w')
            res = json.dump(phoneResult, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()

            print('[PROCESSED] {:s} ({:d}/{:d}) in {:f} secs'.format(deviceName, num, numTotal, (time.time() - startTime)))

# concurrent = 5
# q = Queue(concurrent * 2)

# def phoneProcessingThread():
#     while True:
#         phoneUrl = q.get()
#         processPhone(phoneUrl)
#         # doSomethingWithResult(status, url)
#         q.task_done()

def main(argv):
    phoneUrls = []

    s = requests.Session()
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))

    if ('-p' in argv):
        print("Populating phone list...")

        phonesJson = CrawlUtil.getJSON(s, "http://www.kimonolabs.com/api/4f6q83j4?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN&kimmodify=1")
        for phoneUrl in phonesJson['results']:
            phoneUrls.append(phoneUrl)

        phonesJson = CrawlUtil.getJSON(s, "http://www.kimonolabs.com/api/4f6q83j4?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN&kimmodify=1&kimoffset=2500")
        for phoneUrl in phonesJson['results']:
            phoneUrls.append(phoneUrl)

        phonesJson = CrawlUtil.getJSON(s, "http://www.kimonolabs.com/api/4f6q83j4?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN&kimmodify=1&kimoffset=5000")
        # for phoneUrl in phonesJson['results']:
        #     phoneUrls.append(phoneUrl)

        print("Creating phone_list.txt...")    
        f = open('phones/' + 'phone_list.txt', 'w')
        for phoneUrl in phoneUrls:
            f.write(phoneUrl + '\n')
        f.close()


    # for i in range(concurrent):
    #     t = threading.Thread(target=phoneProcessingThread)
    #     t.daemon = True
    #     t.start()
    # try:
    #     for phoneUrl in open('phones/phone_list.txt'):
    #         print(phoneUrl)
    #         q.put(phoneUrl)
    #     q.join()
    # except KeyboardInterrupt:
    #     sys.exit(1)


    # if ('-p' not in argv):
    print("Loading phone url list from phones/phone_list.txt...")
    processList = open('phones/phone_list.txt', 'r')
    for url in processList:
        phoneUrls.append(url)

    num = 0
    numTotal = len(phoneUrls)
    if ('-nc' not in argv):
        print("Diffing phones/processed.txt and phone url list...")
        processedList = open('phones/processed.txt', 'r')
        for url in processedList:
            if url in phoneUrls:
                phoneUrls.remove(url)
                num += 1

    print("Crawling...")
    for phoneUrl in phoneUrls:
        processPhone(phoneUrl, num, numTotal)
        num += 1

        f = open('phones/processed.txt', 'a')
        f.write(phoneUrl + '\n')
        f.close()

main(sys.argv[1:])
