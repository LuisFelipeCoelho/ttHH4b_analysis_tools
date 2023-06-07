'''
This script plots signal vs bkg distributions from input files from ttHH4banalysis
'''

### config ####

cut_flow = False  # if true plots the cut flow from data-Analysis_EvtSelection instead of variables from data-Analysis_TTHH4B 
nfiles = 10

###############


path = "/afs/cern.ch/user/l/lfaldaul/work/ttHH_analysis/ttHH4banalysis/run/output/"
if cut_flow: postfix = "EvtSelection"
else: postfix = "TTHH4B"

tthh_file = path+"tthh4b-DAOD_PHYSLITE.33100969._000001.pool.root-ttHH_r13167"+"/data-Analysis_{}/mc20_13TeV.523072.MGPy8EG_A14NNPDF23LO_ttHH_semilep.deriv.DAOD_PHYSLITE.e8531_a899_r13167_p5689.root".format(postfix)
ttbar_file = path+"tthh4b-DAOD_PHYSLITE.33100969._000001.pool.root-ttbar"+"/data-Analysis_{}/mc20_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.deriv.DAOD_PHYSLITE.e6337_s3681_r13167_r13146_p5631.root".format(postfix)

mypath1 = "/eos/home-l/lfaldaul/samples/ttHH_analysis/NTRUPLES/ttbar/user.lfaldaul.TTHH4b.410470.e6337_s3681_r13167_r13146_p5631.list_of_files._Analysis_TTHH4B.root/"
mypath2 = "/eos/home-l/lfaldaul/samples/ttHH_analysis/NTRUPLES/ttbar/user.lfaldaul.TTHH4b.410470.e6337_s3681_r13167_r13146_p5631.list_of_files._Analysis_TTHH4B.root/"

from os import listdir
from os.path import isfile, join
tthh_files = [mypath1+f for f in listdir(mypath1) if isfile(join(mypath1, f))]
ttbar_files = [mypath2+f for f in listdir(mypath2) if isfile(join(mypath2, f))]

tthh_files = tthh_files[:nfiles]
ttbar_files = ttbar_files[:nfiles]

files = {
'tthh':tthh_files,
'ttbar':ttbar_files,
}

var = [
 "executedEvents",
 "nmuon",
 "muon_m",
 "muon_pt",
 #"muon_phi",
 "muon_eta",
 "muon_charge",
 "nel",
 "el_m",
 "el_pt",
 #"el_phi",
 "el_eta",
 "el_charge",
 "nrecojet_antikt4",
 "recojet_antikt4_pt",
 "recojet_antikt4_eta",
 #"recojet_antikt4_phi",
 "recojet_antikt4_m",
 "recojet_antikt4_btag77",
 "nrecojet_antikt4_btag77",
 "recojet_antikt4_btag85",
 "nrecojet_antikt4_btag85",
 "recojet_antikt4_btag77_pt",
 "recojet_antikt4_btag77_eta",
 #"recojet_antikt4_btag77_phi",
 "recojet_antikt4_btag77_m",
 "recojet_antikt4_btag85_pt",
 "recojet_antikt4_btag85_eta",
 #"recojet_antikt4_btag85_phi",
 "recojet_antikt4_btag85_m",
 "truthjet_antikt4_pt",
 "truthjet_antikt4_eta",
 #"truthjet_antikt4_phi",
 "truthjet_antikt4_m",
 #"met85_pt",
 #"met85_px",
 #"met85_py",
 "met85_sumet",
 "met85_phi",
]

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
#branch_names = ut.getAllBranchNamesInFile(tthh_files[0], tree_name)
branch_names = var
nEvents = {
'tthh':(ut.getTotalEventsInTree(tthh_files, tree_name)),
'ttbar':(ut.getTotalEventsInTree(ttbar_files, tree_name)),
}

print('Total number of events: ', nEvents['tthh'], nEvents['ttbar'])

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
'nrecojet_antikt4':[13, 0, 13], # all jets
'nrecojet_antikt4_':[10, 0, 10], # b-tagged jets
'recojet_atikt4_btagscore':[16, 0, 16]
}
for key in TH1F_list.keys():
    for branchName in branch_names:
        hist_name = 'TH1F_'+branchName
        hist_config = [30, 0, -1]
        for var, conf in hist_config_values.items():
            if var in branchName: hist_config = conf
        TH1F_list[key][hist_name] = ROOT.TH1F(hist_name, hist_name, hist_config[0], hist_config[1], hist_config[2])

# Fill the histograms
for file_i, (key, file_list) in enumerate(files.items()):

    for file_name in file_list:

        # Read TFile
        print("read TFile " + key + " " + file_name)
        read_file = ROOT.TFile.Open(file_name, "READ")

        # Read TTree
        tree_i = read_file.Get(tree_name)
        print("read TTree", tree_i)

        # Loop over all the branches
        for branchName in branch_names:

            if cut_flow == True and branchName != "trigger_cut_flow":
                continue

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

    if cut_flow == True and branchName != "trigger_cut_flow":
        continue

    hist_name = 'TH1F_'+branchName
    canvas.Clear()

    # Plot
    h1, h2 = pt.plotOptions([TH1F_list['tthh'][hist_name], TH1F_list['ttbar'][hist_name]], "Events", x_label=branchName)
    h1.Draw("h")
    h2.Draw("h same")
    legend = pt.setLegend([h1, h2], ['ttHH MC20a', 'ttbar'], "rightTop", text_plot=['', '', '13 TeV'], yAdd=0.12, xAdd=-0.12)

    canvas.Print(output_path + "/" + branchName + ".png")
    canvas.Print("my_output.pdf")

canvas.Print("my_output.pdf]")
