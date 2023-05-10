'''
Set of root plotting tools
'''

import ROOT

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

