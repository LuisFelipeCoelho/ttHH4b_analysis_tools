'''
This script plots signal vs bkg distributions from input files from ttHH4banalysis
'''

### config ####

cut_flow = False  # if true plots the cut flow from data-Analysis_EvtSelection instead of variables from data-Analysis_TTHH4B 

###############


path = "/afs/cern.ch/user/l/lfaldaul/work/ttHH_analysis/ttHH4banalysis/run/"
if cut_flow: postfix = "EvtSelection"
else: postfix = "TTHH4B"

tthh_file = path+"tthh4b-DAOD_PHYSLITE.32056469._000001.pool.root-test"+"/data-Analysis_{}/mc20_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.deriv.DAOD_PHYSLITE.e6337_s3681_r13167_r13146_p5511.root".format(postfix)
ttbar_file = path+"tthh4b-DAOD_PHYSLITE.32056469._000002.pool.root-test"+"/data-Analysis_{}/mc20_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.deriv.DAOD_PHYSLITE.e6337_s3681_r13167_r13146_p5511.root".format(postfix)

files = {
'tthh':tthh_file,
'ttbar':ttbar_file,
}

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
branch_names = ut.getAllBranchNamesInFile(tthh_file, tree_name)
#nevents = ut.getTotalEventsInTree(files, tree_name)

# Create a dict of histograms for each branch
TH1F_list = {
'tthh':{},
'ttbar':{},
}
hist_config_values = {
    '_p':[30, 0, 500],
    '_m':[30, 0, 80], 
    '_e':[30, 0, 1000],
'_sumet':[30, 0, 2000],
  '_eta':[30, -4, 4],
  '_phi':[30, -4, 4],
'nrecojet_antikt4':[10, 0, 13], # all jets
'nrecojet_antikt4_':[10, 0, 6], # b-tagged jets
}
for key in TH1F_list.keys():
    for branchName in branch_names:
        hist_name = 'TH1F_'+branchName
        hist_config = [30, 0, -1]
        for var, conf in hist_config_values.items():
            if var in branchName: hist_config = conf
        TH1F_list[key][hist_name] = ROOT.TH1F(hist_name, hist_name, hist_config[0], hist_config[1], hist_config[2])

# Fill the histograms
for file_i, (key, file_name) in enumerate(files.items()):

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
                TH1F_list[key][hist_name].Fill(val)

            else:
                for value in val:

                    # Fill histogram
                    hist_name = 'TH1F_'+branchName
                    TH1F_list[key][hist_name].Fill(value)


# Create output directory            
gt.createDir(output_path)

# Create pdf output
canvas = ROOT.TCanvas()
canvas.Print("my_output.pdf[")

# Save the plots
for branchName in branch_names:

    hist_name = 'TH1F_'+branchName
    canvas.Clear()

    # Plot
    h1, h2 = pt.plotOptions(TH1F_list['tthh'][hist_name], TH1F_list['ttbar'][hist_name], "Events", x_label=branchName)
    h1.Draw("h")
    h2.Draw("h same")
    legend = pt.setLegend(h1, h2, "rightTop", text_plot=['ttHH', 'ttbar', '', '', 'PHYSLITE'])

    canvas.Print(output_path + "/" + branchName + ".png")
    canvas.Print("my_output.pdf")

canvas.Print("my_output.pdf]")
