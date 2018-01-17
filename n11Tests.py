#!/usr/bin/python

import requests, json, os, sys, subprocess, time

DIR = os.path.dirname(os.path.realpath(__file__))

#ip = "localhost"
#ip = "192.168.100.36"
ip = sys.argv[1]

baseUrl = "http://%s:8080" % (ip)

returnVal = 0
summary = "\n"
 
#this function will get the n11 translation map(s) 
def getMap(baseUrl, path):
    url = "%s%s" % (baseUrl, path)
    print ("curl -X GET {}".format(url))

    results = requests.get(url).json()
    return results

#this function will add the n11 translation map(s) 
def putMap(baseUrl, path, filename):
    url = "%s%s" % (baseUrl, path)
    headers = "\"Content-Type\":\"application/json\""
#    headers = {'content-type': 'application/json'}
    files = "\'{\"fileName\":\"%s\"}\'" % (filename)
#    files = {"fileName": open(filename, 'rb')}

    print ("curl -X POST -H {} -d {} {}".format(headers, files, url))
    results = os.system("curl -X POST -H {} -d {} {}".format(headers, files, url))
#    results = requests.post(url, files=files, headers=headers)
    print (results)
    print ("\n")

#this function will add the static n11 translation map(s) 
def putStatic(baseUrl, path):
    url = "%s%s" % (baseUrl, path)
    headers = {'content-type': 'application/json'}

    data = {"carriers": [1, 3, 2]}
    print ("curl -X POST -H {} -d {} {}".format(headers, data, url))
    results = requests.post(url, data=json.dumps(data), headers=headers)

    print (results)
    print ("\n")


def sippCall(n11, xml, testName):
    print("\033[94m *** Calling {} {} ***\033[0m".format(n11, testName))
    global returnVal
    global summary

    os.system('export TERM=xterm; sudo ngrep -l -d docker0 -qtW byline sip port 6060 > output &')

    time.sleep(2)

    #843
    print("sipp -sf {} -m 1 -s +{} {}:6060".format(xml, n11, ip))
    os.system("export TERM=xterm; sipp -sf {} -m 1 -s +{} {}:6060 > /dev/null".format(xml, n11, ip))

    time.sleep(5)

    value = 1

    output = open('output', 'r')
    for line in output:
        print(line).rstrip()
        if "SIP/2.0 300 " in line:
            value = 0
            summary = "%s\n \033[92m%s PASSED (%s)" % (summary, n11, testName)
    if value == 1:
        returnVal = 1
        summary = "%s\n \033[91m%s FAILED (%s)" % (summary, n11, testName)

    print("Returned: {}").format(value)

    os.system('sudo killall ngrep')
    time.sleep(10)

    output.close() 
    os.remove('output')

def main():
    global returnVal
    global summary
    print ("Using base url: {}\n".format(baseUrl))
    summary = "\nUsing base url: {}\n".format(baseUrl)

##    path = "/n11/translationMaps/upload"
##    results = putMap(baseUrl, path, "/home/router/testMap.csv")
##    print results
#
#    path = "/n11/211/activeTranslationMap"
#    results = putMap(baseUrl, path, "/home/router/testMap.csv")
#    print results
#
#    path = "/n11/translationMaps/"
#    results = getMap(baseUrl, path)
#    print results
#
#    path = "/n11/translationMaps/"
#    results = putMap(baseUrl, path, "testMap.csv")
#    print results
#
#    path = "/n11/translationMaps/"
#    results = getMap(baseUrl, path)
#    print results
#
#    path = "/n11/translationMaps/?name=testMap.csv"
#    results = getMap(baseUrl, path)
#    print results
#
#    path = "/n11/translationMaps/active"
#    results = getMap(baseUrl, path)
#    print results
#
##    path = "/n11/211/translationMaps/active"
##    results = getMap(baseUrl, path)
##    print results


    collection = ['211','511','811']
    for n11 in collection:
        path = "/n11/{}/activeTranslationMap".format(n11)
        results = getMap(baseUrl, path)
        print results

        # If there isn't a map add one
        if 'errorCode' in results: 
            print ("no map")
            filename = "/home/router/testMap.csv"
            putMap(baseUrl, path, filename) 
        
        # No Rate Deck (PASS)
#        sippCall(n11, DIR + "/xml/MRD.xml", "No Rate Deck")
        # Rate Deck But No Rate (FAIL)
#        sippCall(n11, DIR + "/xml/unmapped.xml", "Rate Deck Without Rate")
        # Rate Deck With Rate (PASS)
        sippCall(n11, DIR + "/xml/mapped.xml", "Rate Deck With Rate")


    collection = ['311','611','711','911']
    for n11 in collection:
        path = "/n11/{}/staticCarriers".format(n11)
        results = getMap(baseUrl, path)
        print results

        # If there isn't a map add one
        if len(results['carriers']) == 0: 
            print ("no map")
            putStatic(baseUrl, path) 

        # No Rate Deck (PASS)
        sippCall(n11, DIR + "/xml/MRD.xml", "No Rate Deck")
        # Rate Deck But No Rate (FAIL)
#        sippCall(n11, DIR + "/xml/unmapped.xml", "Rate Deck Without Rate")
        # Rate Deck With Rate (PASS)
        sippCall(n11, DIR + "/xml/mapped.xml", "Rate Deck With Rate")

    print("return value: {}".format(returnVal))
    print("\nSummary:{}\033[0m\n\n").format(summary)
    sys.exit(returnVal)

main()
