#!/usr/bin/env python3
# TODO RS-1: Generalization, cut URLs down regardless of content

__author__ = "Ryan Squires"
__version__ = "0.2"
__license__ = "GPL-3.0-or-later"

import re
from urllib.parse import urlparse

def regexStringsCompile():
    # regex search string compiles
    verComp = re.compile(r" ver\d")
    acousComp = re.compile(" acoustic", re.IGNORECASE)
    return verComp, acousComp

def readFile():
    # read in dead bookmarks from file
    bkmks = open("dead_bookmarks_example.txt", "r")
    artistSongList = bkmks.readlines()
    bkmks.close()
    return artistSongList

def cleanURLs(deadBookmarks): # string cleanup loop
    verComp, acousComp = regexStringsCompile()

    pathList = []
    for line in deadBookmarks:
        # parse
        url = urlparse(line)

        #initial strip
        path = url.path.strip(' /\n')

        # strip starting '[a-z]/'
        slashCleanIdx = path.find('/')
        if slashCleanIdx == 1 : path = path[slashCleanIdx + 1:]
        
        # replace underscores with space
        path = path.replace('_', ' ')
        
        # remove end-of-string garbage
        # TODO RS-1
        # remove 'crd'
        crdIdx = path.rfind(' crd')
        if crdIdx != -1 : path = path[:crdIdx] 
        
        # remove 'tab'
        tabIdx = path.rfind(' tab')
        if tabIdx != -1 : path = path[:tabIdx]
        
        # RE remove 'ver#'
        verSearch = verComp.search(path)
        if verSearch :
            verIdx = verSearch.start()
            path = path[:verIdx]
        
        # RE remove 'acoustic'
        acousSearch = acousComp.search(path)
        if acousSearch :
            acousIdx = acousSearch.start()
            path = path[:acousIdx]

        # split at '/', tuplify, and append to list
        pathList.append(tuple(path.split('/')))
    
    # remove duplicates and sort
    sortedList = sorted(list(set(pathList)))

    # create artists:[songs] formatted dict
    sortedDict = {}
    for i, j in sortedList : sortedDict.setdefault(i, []).append(j)
    
    return sortedDict

def writeFile(finalDict) :
    # format dict and output to file
    cleanedBkmks = open("cleaned_example.txt", "w")
    cleanedBkmks.write(f"{'Artist':<32}Songs\n\n")
    for key, valueList in finalDict.items():
        valueString = str(", ".join(valueList))
        cleanedBkmks.write(f"{key:<32}{valueString}\n")
    cleanedBkmks.close()

def main():
    inputFile = readFile()
    cleanedDict = cleanURLs(inputFile)
    writeFile(cleanedDict)

if __name__ == "__main__":
    main()