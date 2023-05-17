'''
Set of root plotting tools
'''

import ROOT

ROOT.gROOT.SetStyle("ATLAS")

def simplePlot(hist1, xLabel, yLabel='Events'):
	'''
	Plot a TH1F histogram 
	'''
	hist1.GetYaxis().SetTitleSize(20)
	hist1.GetYaxis().SetTitleFont(43)
	hist1.GetYaxis().SetTitleOffset(1.7)
	hist1.GetYaxis().SetTitle(yLabel)
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

def simpleLegend(hist1, nevents, event_name="", sqrt_s='13.6 TeV'):
	'''
	Adds legend to histogram (number of events, event name and center-of-mass enery)
	'''
	#legend = ROOT.TLegend(0.57,0.65,0.90,0.72)
	#legend.AddEntry(hist1 ,"t#bar{t}HH SM truth level")
	#legend.SetTextSize(0.035)
	#legend.SetLineWidth(0)
	#legend.SetFillStyle(0)
	#legend.Draw("same")
	latex = ROOT.TLatex()
	latex.SetNDC()
	latex.SetTextSize(0.035)
	latex.DrawText(0.58, 0.80, event_name)
	latex.DrawLatex(0.58, 0.85, str(nevents) + " events, #sqrt{s} = {}".format(sqrt_s))
	#latex.DrawText(0.58, 0.75, "AthGeneration 23.6.0")

def setLegend(acts, orthogonal, right="rightTop"):
	if right=="rightTop":	legend = ROOT.TLegend(0.6,0.65,0.95,0.72)
	elif right=="leftTop":  legend = ROOT.TLegend(0.2,0.65,0.55,0.72)
	elif right=="leftBot":  legend = ROOT.TLegend(0.2,0.15,0.55,0.22)
	elif right=="rightBot": legend = ROOT.TLegend(0.6,0.15,0.95,0.22)
	legend.AddEntry(acts ,"ACTS reference"+time_default)
	legend.AddEntry(orthogonal ,"ACTS monitored"+time_orthogonal)
	legend.SetTextSize(0.035)
	legend.SetLineWidth(0)
	legend.SetFillStyle(0)
	legend.Draw("same")
	latex = ROOT.TLatex()
	latex.SetNDC()
	latex.SetTextSize(0.035)
	if right=="rightTop":
		latex.DrawText(0.61, 0.80, " ITk {} configuration".format(detector))
		latex.DrawLatex(0.61, 0.85, text_plot)
		latex.DrawText(0.61, 0.75, nEventTotal)
	elif right=="leftTop":
		latex.DrawText(0.21, 0.80, " ITk {} configuration".format(detector))
		latex.DrawLatex(0.21, 0.85, text_plot)
		latex.DrawText(0.21, 0.75, nEventTotal)	
	elif right=="leftBot":
		latex.DrawText(0.21, 0.30, " ITk {} configuration".format(detector))
		latex.DrawLatex(0.21, 0.35, text_plot)
		latex.DrawText(0.21, 0.25, nEventTotal)	
	elif right=="rightBot":
		latex.DrawText(0.61, 0.30, " ITk {} configuration".format(detector))
		latex.DrawLatex(0.61, 0.35, text_plot)
		latex.DrawText(0.61, 0.25, nEventTotal)	
	return legend

def setLegend2(h1, name):
	'''
	Draw entry to legend
	'''
	legend2.AddEntry(h1 , name)
	legend2.SetLineWidth(0)
	legend2.SetFillStyle(0)
	legend2.Draw("same")
 
def plotOptions(h1, h2, y_label, yMin=-1, yMax=-1):
	'''
	Set plotting configuration
	'''
	h1.GetYaxis().SetTitle(y_label)
	h1.GetYaxis().SetLabelSize(0.);
	h1.SetLineColor(206)
	h2.SetLineColor(62)
	h1.SetLineWidth(2)
	h1.SetMarkerStyle(0);
	h2.SetMarkerStyle(0);
	h1.GetYaxis().SetTitleSize(20)
	h1.GetYaxis().SetTitleFont(43)
	h1.GetYaxis().SetTitleOffset(3)
	h1.GetYaxis().SetLabelFont(43)
	h1.GetYaxis().SetLabelSize(15)
	h1.GetXaxis().SetLabelFont(43)
	h1.GetXaxis().SetLabelSize(15)
	h2.GetXaxis().SetRange(1,40)
	h1.GetXaxis().SetRange(1,40)
	if yMin != -1:
		h1.GetYaxis().SetRangeUser(yMin,yMax)
		h2.GetYaxis().SetRangeUser(yMin,yMax)
	h1.SetStats(0)
	h2.SetLineWidth(2)
	return h1, h2

def createPad1(logY=False, gridX=False):
	'''
	Create top root pad 
	'''
	pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
	pad1.SetBottomMargin(0.05)
	if gridX: pad1.SetGridx()
	if logY: pad1.SetLogy()
	pad1.Draw()
	pad1.cd()
	return pad1

def createPad2(gridX=False):
	'''
	Create bottom root pad
	'''
	pad2 = ROOT.TPad("pad2", "pad2", 0, 0.08, 1, 0.3)
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	if gridX: pad1.SetGridx()
	pad2.Draw()
	pad2.cd()
	return pad2

def createCanvasPads():
	'''
	Create a canvas with a top histogram and a bottom ratio plot
	'''
	c = ROOT.TCanvas("c", "canvas", 800, 800)
	# Upper histogram plot is pad1
	pad1 = createPad1()
	# Lower ratio plot is pad2
	c.cd()
	pad2 = createPad2()
	return c, pad1, pad2

def plotRatio(h1, h2, x_label):
	'''
	Create ratio plot from two TH1F histograms
	'''

	# Define the ratio plot
	h3 = h1.Clone("h3")
	h3.SetTitle("")
	h3.SetLineColor(1)
	h3.SetMinimum(0.8)
	h3.SetMaximum(1.35)
	h3.SetMarkerStyle(21)
	h3.Sumw2()
	h3.SetStats(0)
	h3.Divide(h2)

	# Y axis h1 plot settings
	h1.GetYaxis().SetTitleSize(20)
	h1.GetYaxis().SetTitleFont(43)
	h1.GetYaxis().SetTitleOffset(1.6)

	# Y axis ratio plot settings
	h3.GetYaxis().SetTitle("")
	h3.GetYaxis().SetNdivisions(505)
	h3.GetYaxis().SetTitleSize(20)
	h3.GetYaxis().SetTitleFont(43)
	h3.GetYaxis().SetTitleOffset(1.6)
	h3.GetYaxis().SetLabelFont(43)
	h3.GetYaxis().SetLabelSize(15)

	# X axis ratio plot settings
	h3.GetXaxis().SetTitle(x_label)
	h3.GetXaxis().SetTitleSize(20)
	h3.GetXaxis().SetTitleFont(43)
	h3.GetXaxis().SetTitleOffset(1)
	h3.GetXaxis().SetLabelFont(43)
	h3.GetXaxis().SetLabelSize(15)

	return h3


