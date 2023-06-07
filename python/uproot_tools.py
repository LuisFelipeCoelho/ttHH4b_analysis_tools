'''
Set of uproot tools
'''

import ROOT
import uproot


def getAllBranchNamesInFile(filePath, tree_name):
    '''
    Get branch names from file path
    '''
    file_uproot = uproot.open(filePath)
    file_uproot.classnames()
    file_uproot[tree_name].show()

    return file_uproot[tree_name].keys()


def getTotalEventsInTree(filePathList, tree_name):
    '''
    Calculate total number of events in all files from a list with file paths 
    '''
    nevents = 0
    if type(filePathList) == list:
        for file_i, file_name in enumerate(filePathList):
            file_uproot_i = uproot.open(filePathList[file_i])
            nevents += len(file_uproot_i[tree_name].arrays("runNumber", library="pd"))
    if type(filePathList) == str:
        file_uproot_i = uproot.open(filePathList)
        nevents += len(file_uproot_i[tree_name].arrays("runNumber", library="pd"))

    return nevents
