'''
This script plots all the branches from several input files from ttHH4banalysis
'''

### config ####

number_of_files = 2	# number of files to run
cut_flow = False	# if true plots the cut flow from data-Analysis_EvtSelection instead of variables from data-Analysis_TTHH4B 

###############


path = "/afs/cern.ch/user/l/lfaldaul/work/ttHH_analysis/ttHH4banalysis/run/"
if cut_flow: postfix = "EvtSelection"
else: postfix = "TTHH4B"
files = [path+"tthh4b-DAOD_PHYSLITE.32056469._{0:06}.pool.root-test".format(n_file+1)+"/data-Analysis_{}/mc20_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.deriv.DAOD_PHYSLITE.e6337_s3681_r13167_r13146_p5511.root".format(postfix) for n_file in range(number_of_files)]

tree_name = "MiniTree_NOSYS"
output_path = "../figs/plots_hh4b"
outputFileName = "../figs/plots_hh4b.png"

import sys
import numpy as np
import ROOT
import os
import uproot
import pandas as pd
import plotting_tools as pt
import uproot_tools as ut
import general_tools as gt

ROOT.gROOT.SetStyle("ATLAS")

# Get name of branches and total number of events
branch_names = ut.getAllBranchNamesInFile(files[0], tree_name)
nevents = ut.getTotalEventsInTree(files, tree_name)

# Create a dict of histograms for each branch
TH1F_list = {}
for branchName in branch_names:
    hist_name = 'TH1F_'+branchName
    TH1F_list[hist_name] = ROOT.TH1F(hist_name, hist_name, 30, 0, -1)

# Fill the histograms
for file_i, file_name in enumerate(files):

    # Read TFile
    print("read TFile " + file_name)
    read_file = ROOT.TFile.Open(file_name, "READ")

    # Read TTree
    tree_i = read_file.Get(tree_name)
    print("read TTree", tree_i)

    # Loop over all the branches
    for branchName in branch_names:

        # Read the branch
        print("read branch: " + branchName)
        branch = tree_i.GetBranch(branchName)

        # Loop over all the entries in file
        for entry in tree_i:

            # Read entry
            val = getattr(entry, branchName)

            # Check if val is int or float
            if isinstance(val, (int, float)):

                # Fill histogram
                hist_name = 'TH1F_'+branchName
                TH1F_list[hist_name].Fill(val)

            else:
                for value in val:

                    # Fill histogram
                    hist_name = 'TH1F_'+branchName
                    TH1F_list[hist_name].Fill(value)

# Create output directory            
gt.createDir(output_path)

# Create pdf output
canvas = ROOT.TCanvas()
canvas.Print("my_output.pdf[")

# Save the plots
for branchName in branch_names:

    hist_name = 'TH1F_'+branchName
    canvas.Clear()
    pt.simplePlot(TH1F_list[hist_name], branchName)
    pt.simpleLegend(TH1F_list[hist_name], nevents, event_name="Physlite ttbar")
    canvas.Print(output_path + "/" + branchName + ".png")
    canvas.Print("my_output.pdf")

canvas.Print("my_output.pdf]")
