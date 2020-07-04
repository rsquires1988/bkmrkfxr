#!/usr/bin/env python3
"""
# TODO 2, add module names, see todo 1
"""

__author__ = "Ryan Squires"
__version__ = "0.1.1"
__license__ = "GPL-3.0-or-later"

import re
from urllib.parse import urlparse

# TODO 1: modularize
def main():
    # regex search string compiles
    verComp = re.compile(r" ver\d")
    acousComp = re.compile(" acoustic", re.IGNORECASE)

    # read in dead bookmarks from file
    bkmks = open("dead_bookmarks_example.txt", "r")
    artistSongList = bkmks.readlines()
    bkmks.close()

    # string cleanup loop
    pathList = []
    for line in artistSongList:
        # parse and basic strip
        url = urlparse(line)

        #initial strip
        path = url.path.strip(' /\n')

        # strip 
        slashCleanIdx = path.find('/')
        if slashCleanIdx == 1 : path = path[slashCleanIdx + 1:]
        
        # replace underscores with space
        path = path.replace('_', ' ')
        
        # remove end garbage
        # TODO 5: Potential bug if path doesn't contain ' crd' or ' tab'
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
    pathSet = sorted(list(set(pathList)))
    
    # create artists:[songs] formatted dict
    dictBkmks = {}
    for i, j in pathSet : dictBkmks.setdefault(i, []).append(j)

    # format dict and output to file
    cleanedBkmks = open("cleaned_example.txt", "w")
    cleanedBkmks.write(f"{'Artist':<32}Songs\n\n")
    for key, valueList in dictBkmks.items():
        valueString = str(", ".join(valueList))
        cleanedBkmks.write(f"{key:<32}{valueString}\n")
    cleanedBkmks.close()

if __name__ == "__main__":
    main()