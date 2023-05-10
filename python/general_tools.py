'''
Set of general tools
'''
import ROOT
import os

import time
global_time = time.time()
counter = 0

def createDir(dirName):
    '''
    Creates a new directory
    '''
    try:
        os.mkdir(dirName)
    except OSError as error:
        print(error)


def timer(reset=False):
    '''
    To measure wall time 
    '''
    global counter
    global global_time
    if reset:
        global_time = time.time()
        counter = 0
    else:
        print('At counter {}, {} has passed'.format(counter, time.time()-global_time))
        counter += 1


def check4Branch(filename, treename, branchname):
    '''
    Check if branch exists 
    '''
    if not tfile_exists(filename, check_grid_filepath=True):
        print('The file {} does not exist'.format(filename))
        return False
    f = TFile(filename, "READ")
    t = f.Get(treename)
    branch = t.GetBranch(branchname)
    return True if branch else False
