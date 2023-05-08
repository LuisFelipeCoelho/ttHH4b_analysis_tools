file = "/afs/cern.ch/user/l/lfaldaul/work/ttHH_analysis/ttHH4banalysis/run/sh4b-DAOD_PHYSLITE.32056469._000001.pool.root-test/data-Analysis_SH4B/mc20_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.deriv.DAOD_PHYSLITE.e6337_s3681_r13167_r13146_p5511.root"

tree_name = "MiniTree_NOSYS"
output_path = "../figs/plots_hh4b"
outputFileName = "../figs/plots_hh4b.png"

import sys
import numpy as np
import ROOT
import os
import uproot
import pandas as pd

ROOT.gROOT.SetStyle("ATLAS")

def simplePlot(hist1, xLabel):
    hist1.GetYaxis().SetTitleSize(20)
    hist1.GetYaxis().SetTitleFont(43)
    hist1.GetYaxis().SetTitleOffset(1.7)
    hist1.GetYaxis().SetTitle("Events")
    hist1.GetXaxis().SetTitle(xLabel)
    hist1.GetYaxis().SetLabelSize(0.)
    hist1.SetLineColor(206)
    hist1.SetLineWidth(2)
    hist1.SetMarkerStyle(0)
    hist1.GetYaxis().SetTitleSize(15)
    hist1.GetYaxis().SetTitleFont(43)
    hist1.GetXaxis().SetTitleOffset(0.7)
    hist1.GetYaxis().SetLabelFont(43)
    hist1.GetYaxis().SetLabelSize(15)
    hist1.GetXaxis().SetLabelFont(43)
    hist1.GetXaxis().SetLabelSize(15)
    hist1.GetXaxis().SetRange(1,40)
    hist1.SetStats(1) 
    hist1.Draw("he")
    
def simpleLegend(hist1, nevents):
    legend = ROOT.TLegend(0.57,0.65,0.90,0.72)
    legend.AddEntry(hist1 ,"t#bar{t}HH SM truth level")
    legend.SetTextSize(0.035)
    legend.SetLineWidth(0)
    legend.SetFillStyle(0)
    legend.Draw("same")
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.DrawText(0.58, 0.80, "Physlite ttbar")
    latex.DrawLatex(0.58, 0.85, str(nevents) + " events, #sqrt{s} = 13.6 TeV")
    #latex.DrawText(0.58, 0.75, "AthGeneration 23.6.0")

print("read TFile " + file)
read_file = ROOT.TFile.Open(file, "READ")

tree = read_file.Get(tree_name)
print("read TTree", tree)

file_uproot = uproot.open(file)
file_uproot.classnames()
file_uproot['MiniTree_NOSYS'].show()
branche_names = file_uproot['MiniTree_NOSYS'].keys()
nevents = len(file_uproot['MiniTree_NOSYS'].arrays("runNumber", library="pd"))

def createDir(dirName):
	try: 
		os.mkdir(dirName) 
	except OSError as error: 
        	print(error)
            
createDir(output_path)

canvas = ROOT.TCanvas()
canvas.Print("my_output.pdf[")
for branchName in branche_names:
    canvas.Clear()
    histo1 = ROOT.TH1F('histo1', 'histo1', 30, 0, -1)
    tree.Project('histo1', branchName)
    simplePlot(histo1, branchName)
    simpleLegend(histo1, nevents)
    canvas.Print(output_path + "/" + branchName + ".png")
    canvas.Print("my_output.pdf")
canvas.Print("my_output.pdf]")

