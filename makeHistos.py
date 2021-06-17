import os
import sys
import re
import math
import numpy as np
import ROOT
import argparse
import numpy as np
from array import array
import PoissErr

### python makeHistos.py --postfit /afs/cern.ch/work/f/fernanpe/framework_monoHFullRun2/CMSSW_10_2_9/src/PlotsConfigurations/Configurations/monoHWW/Full2017_v7_3d/fitDiagnostics.root --year 2017

parser = argparse.ArgumentParser(description='Make custom plots')
parser.add_argument('--postfit', action='store', dest='postfit', default = 'fitDiagnostics.root', help='Combine FitDiagnostics file. Need to be run with --saveShapes --saveNormalizations --saveWithUncertainties')
parser.add_argument('--year', action='store', dest='year', help='data period')
args = parser.parse_args()

sys.argv = []

SRs = ["ch1","ch2","ch3"]

ROOT.TH1.SetDefaultSumw2(True)

#### Define the real binning

if args.year == '2016':
    drll = [0.0,0.5,1.5,2.5]
    mll = [12,60,90,120,200]
    mt = np.array([0,50,90,130,160,300], dtype='float64')
elif args.year == '2017':
    drll = [0.0,0.5,1.5,2.5]
    mll = [12,60,90,120,200]
    mt = np.array([0,50,90,130,170,300], dtype='float64')
elif args.year == '2018':
    drll = [0.0,0.5,1.5,2.5]
    mll = [12,60,90,120,200]
    mt = np.array([0,50,90,130,180,300], dtype='float64')

#### OPEN the input file

file_input = ROOT.TFile(args.postfit)

sigs = ["total_signal"]
bkgs = ["DY","Fake","Higgs","VVV","VZ","Vg","VgS","WW","WWewk","ggWW","top"]

histos_sigs=[]

histos_DY=[]
histos_qqWW=[]
histos_top=[]
histos_Fake=[]
histos_Higgs=[]
histos_VVV=[]
histos_VZ=[]
histos_Vg=[]
histos_VgS=[]
histos_ggWW=[]
histos_WWewk=[]

histos_WW=[]
histos_Others=[]
histos_data = []
histos_bkg = []

for SR in SRs:
    histos_sigs.append(file_input.Get('shapes_prefit/' + SR + '/total_signal'))
    histos_DY.append(file_input.Get('shapes_fit_s/' + SR + '/DY'))
    histos_top.append(file_input.Get('shapes_fit_s/' + SR + '/top'))
    histos_Fake.append(file_input.Get('shapes_fit_s/' + SR + '/Fake'))
    histos_Higgs.append(file_input.Get('shapes_fit_s/' + SR + '/Higgs'))
    histos_VVV.append(file_input.Get('shapes_fit_s/' + SR + '/VVV'))
    histos_qqWW.append(file_input.Get('shapes_fit_s/' + SR + '/WW'))
    histos_VZ.append(file_input.Get('shapes_fit_s/' + SR + '/VZ'))
    histos_Vg.append(file_input.Get('shapes_fit_s/' + SR + '/Vg'))
    histos_VgS.append(file_input.Get('shapes_fit_s/' + SR + '/VgS'))
    histos_WWewk.append(file_input.Get('shapes_fit_s/' + SR + '/WWewk'))
    histos_ggWW.append(file_input.Get('shapes_fit_s/' + SR + '/ggWW'))
    histos_data.append(file_input.Get('shapes_fit_s/' + SR + '/data'))
    histos_bkg.append(file_input.Get('shapes_fit_s/' + SR + '/total_background'))


#### Set Real mT bins

mt_sig=[]
mt_WW=[]
mt_Fake=[]
mt_Higgs=[]
mt_top=[]
mt_DY=[]
mt_Others=[]
mt_bkg=[]
mt_data=[]

data_y=[]
data_y_errlow=[]
data_y_errhigh=[]


for i in range(0,len(SRs)):
    list_WW = ROOT.TList()
    list_WW.Add(histos_qqWW[i])
    list_WW.Add(histos_ggWW[i])
    list_WW.Add(histos_WWewk[i])

    list_other = ROOT.TList()
    list_other.Add(histos_VVV[i])
    list_other.Add(histos_VZ[i])
    list_other.Add(histos_Vg[i])
    list_other.Add(histos_VgS[i])

    temp1=histos_qqWW[0].Clone('temp')
    temp1.Reset()
    temp1.Merge(list_WW)
    histos_WW.append(temp1)

    temp2=histos_qqWW[0].Clone('temp')
    temp2.Reset()
    temp2.Merge(list_other)
    histos_Others.append(temp2)

    del list_WW,list_other,temp1,temp2


for sr in range(0,len(SRs)):
    for j in range(0,len(mll)-1):
        temp_sig = ROOT.TH1F('histo_sig_' + str(sr) + '_' + str(j),'histo_sig_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_WW = ROOT.TH1F('histo_WW_' + str(sr) + '_' + str(j),'histo_WW_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_Fake = ROOT.TH1F('histo_Fake_' + str(sr) + '_' + str(j),'histo_Fake_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_Higgs = ROOT.TH1F('histo_Higgs_' + str(sr) + '_' + str(j),'histo_Higgs_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_top = ROOT.TH1F('histo_top_' + str(sr) + '_' + str(j),'histo_top_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_DY = ROOT.TH1F('histo_DY_' + str(sr) + '_' + str(j),'histo_DY_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_Others = ROOT.TH1F('histo_Others_' + str(sr) + '_' + str(j),'histo_Others_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        temp_bkg = ROOT.TH1F('histo_bkg_' + str(sr) + '_' + str(j),'histo_bkg_' + str(sr) + '_' + str(j),len(mt)-1,mt)
        y = array( 'd' )
        y_errlow, y_errhigh  = array( 'd' ), array( 'd' )
        for i in range(1,len(mt)):
            temp_sig.SetBinContent(i,histos_sigs[sr].GetBinContent(5*j+i))
            temp_sig.SetBinError(i,histos_sigs[sr].GetBinError(5*j+i))
            temp_WW.SetBinContent(i,histos_WW[sr].GetBinContent(5*j+i))
            temp_WW.SetBinError(i,histos_WW[sr].GetBinError(5*j+i))
            temp_Fake.SetBinContent(i,histos_Fake[sr].GetBinContent(5*j+i))
            temp_Fake.SetBinError(i,histos_Fake[sr].GetBinError(5*j+i))
            temp_Higgs.SetBinContent(i,histos_Higgs[sr].GetBinContent(5*j+i))
            temp_Higgs.SetBinError(i,histos_Higgs[sr].GetBinError(5*j+i))
            temp_top.SetBinContent(i,histos_top[sr].GetBinContent(5*j+i))
            temp_top.SetBinError(i,histos_top[sr].GetBinError(5*j+i))
            temp_DY.SetBinContent(i,histos_DY[sr].GetBinContent(5*j+i))
            temp_DY.SetBinError(i,histos_DY[sr].GetBinError(5*j+i))
            temp_Others.SetBinContent(i,histos_Others[sr].GetBinContent(5*j+i))
            temp_Others.SetBinError(i,histos_Others[sr].GetBinError(5*j+i))
            temp_bkg.SetBinContent(i,histos_bkg[sr].GetBinContent(5*j+i))
            temp_bkg.SetBinError(i,histos_bkg[sr].GetBinError(5*j+i))
            y.append(histos_data[sr].GetPointY(5*j+i-1))
            y_errlow.append(PoissErr.GetPoissError(histos_data[sr].GetPointY(5*j+i-1),1,0))
            y_errhigh.append(PoissErr.GetPoissError(histos_data[sr].GetPointY(5*j+i-1),0,1))
        mt_sig.append(temp_sig)
        mt_WW.append(temp_WW)
        mt_Fake.append(temp_Fake)
        mt_Higgs.append(temp_Higgs)
        mt_top.append(temp_top)
        mt_DY.append(temp_DY)
        mt_Others.append(temp_Others)
        mt_bkg.append(temp_bkg)
        data_y.append(y)
        data_y_errlow.append(y_errlow)
        data_y_errhigh.append(y_errhigh)
        del temp_sig,temp_WW,temp_Fake,temp_Higgs,temp_top,temp_DY,temp_Others,temp_bkg,y,y_errlow,y_errhigh
 

#### CREATE DATA TGraphAsymmErrors OBJECTS

data_x = array( 'd' )
data_x_binwidth = array( 'd' )

for i in range(1,len(mt)):
    data_x.append(mt_sig[0].GetBinCenter(i))
    data_x_binwidth.append(mt_sig[0].GetBinWidth(i)/2.0)


names = {
  "0": "0_0",
  "1": "0_1",
  "2": "0_2",
  "3": "0_3",
  "4": "1_0",
  "5": "1_1",
  "6": "1_2",
  "7": "1_3",
  "8": "2_0",
  "9": "2_1",
  "10": "2_2",
  "11": "2_3",
}

for i in range(0,len(SRs)*(len(mll)-1)):
    if data_y[i] == 0:
        temp = ROOT.TGraphAsymmErrors(len(mt)-1,data_x,data_y[i],data_x_binwidth,data_x_binwidth,0,data_y_errhigh[i])
    else:
        temp = ROOT.TGraphAsymmErrors(len(mt)-1,data_x,data_y[i],data_x_binwidth,data_x_binwidth,data_y_errlow[i],data_y_errhigh[i])
    temp.SetName('histo_data_' + names.get(str(i)))
    mt_data.append(temp)
    del temp


##### COMPUTE RATIOS

mt_ratio = []
mt_ratio_mc = []

for i in range(0,len(SRs)*(len(mll)-1)):
    
    temp_ratio =  ROOT.TGraphAsymmErrors()
    temp_ratio.SetName('histo_ratio_' + names.get(str(i)))

    temp_ratio_mc =  ROOT.TGraphAsymmErrors()
    temp_ratio_mc.SetName('histo_ratioMC_' + names.get(str(i)))


    for ip in range(mt_data[0].GetN()):
        temp_ratio.SetPoint(ip, mt_data[i].GetX()[ip], mt_data[i].GetY()[ip] / mt_bkg[i].GetBinContent(ip+1))
        temp_ratio.SetPointError(ip, mt_data[i].GetErrorXlow(ip), mt_data[i].GetErrorXhigh(ip), PoissErr.GetPoissError(mt_data[i].GetY()[ip], 1, 0) / mt_bkg[i].GetBinContent(ip+1), PoissErr.GetPoissError(mt_data[i].GetY()[ip] , 0, 1) / mt_bkg[i].GetBinContent(ip+1))

        temp_ratio_mc.SetPoint(ip, mt_data[i].GetX()[ip], 1.0)
        temp_ratio_mc.SetPointError(ip, mt_data[i].GetErrorXlow(ip), mt_data[i].GetErrorXhigh(ip), mt_bkg[i].GetBinError(ip+1) / mt_bkg[i].GetBinContent(ip+1), mt_bkg[i].GetBinError(ip+1) / mt_bkg[i].GetBinContent(ip+1))

    mt_ratio.append(temp_ratio)
    mt_ratio_mc.append(temp_ratio_mc)

    del temp_ratio,temp_ratio_mc


##### SAVE HISTOGRAMS 

out_file = ROOT.TFile('out_' + args.year +'.root','recreate')

out_file.cd()

for i in range(0,len(SRs)*(len(mll)-1)):
    mt_data[i].Write()
    mt_sig[i].Write()
    mt_WW[i].Write()
    mt_Fake[i].Write()
    mt_Higgs[i].Write()
    mt_top[i].Write()
    mt_DY[i].Write()
    mt_Others[i].Write()
    mt_bkg[i].Write()
    mt_ratio[i].Write()
    mt_ratio_mc[i].Write()

out_file.Close()

# mt_stacks = []

# # BUILD THE STACK HISTOGRAM

# for i in range(0,len(mt_data)):
#     temp_stack = ROOT.THStack()    
#     temp_stack.Add(mt_WW[i])
#     temp_stack.Add(mt_Fake[i])
#     temp_stack.Add(mt_Higgs[i])
#     temp_stack.Add(mt_top[i])
#     temp_stack.Add(mt_DY[i])
#     temp_stack.Add(mt_Others[i])
    
#     mt_stacks.append(temp_stack)
#     del temp_stack

# _temporaries = []

# nrow = 6
# ncol = 2

# canvas = common.makeRatioCanvas(600, 680, dataset='2017', panels=(ncol, nrow), legend_inside=False, prelim=False)

# canvas.xaxis.SetTitle('#font[12]m_{T}^{l_{min}, p_{T}^{miss}} (GeV)')
# canvas.xaxis.SetNdivisions(408)
# #canvas.ratiotext = 'Background subtracted'

# # symbols = {
# #     'mll_drll1': '#font[12]{m}_{#kern[-0.3]{ll}},{\DeltaR}_{#kern[-0.3]{ll} < 0.5}',
# #     'mll_drll2': '#font[12]{m}_{#kern[-0.3]{ll}},0.5 < {\DeltaR}_{#kern[-0.3]{ll} < 1.5}',
# #     'mll_drll3': '#font[12]{m}_{#kern[-0.3]{ll}},1.5 < {\DeltaR}_{#kern[-0.3]{ll} < 2.5}',
# # }

# # for iplot in range(0,(len(drll)-1)*(len(mll)-1)):
# #     icol = iplot % ncol
# #     irow = nrow - iplot / ncol - 1
# #     print "plot", iplot
# #     print irow
# #     print icol
# #     if iplot == 1:
# #         print(tuple(mll[iplot:iplot + 2]))
# #    canvas.panel_labels[(icol, irow)] = '%.0f < {mll_drll1} < %.0f GeV'.format(**symbols) % tuple(mll[iplot:iplot + 2])
# #    if iplot != len(mll) - 1:
# #        canvas.panel_labels[(icol, irow)] = '%.0f < {mll_drll1} < %.0f GeV'.format(**symbols) % tuple(mll[iplot:iplot + 2])
# #    else:
# #        canvas.panel_labels[(icol, irow)] = '{mll_drll1} > %.0f GeV'.format(**symbols) % mll[iplot]


# zero = ROOT.TLine(0., 0., 1., 1.)
# _temporaries.append(zero)
# zero.SetLineColor(ROOT.kBlack)
# zero.SetLineWidth(1)
# zero.SetLineStyle(ROOT.kSolid)


# def plotstack(stacks, signals, uncerts, gobss, irow):
#     ymax = 0.
#     rmin = 0.
#     rmax = 0.
#     for icol in range(ncol):
#         gobs = gobss[icol]
#         uncert = uncerts[icol]
#         signal = signals[icol]

#         obsmax = max(gobs.GetY()[ip] + gobs.GetErrorYhigh(ip) for ip in range(gobs.GetN()))
#         uncmax = max(uncert.GetBinContent(ix) + uncert.GetBinError(ix) for ix in range(1, uncert.GetNbinsX() + 1))
#         ymax = max(ymax, obsmax, uncmax)

#         obsarray = rnp.array(ROOT.TArrayD(gobs.GetN(), gobs.GetY()))
#         bkg = rnp.hist2array(uncert)
#         bkg -= rnp.hist2array(signal, copy=False)
#         obsarray -= bkg

#         mm = obsarray.min() - gobs.GetErrorYlow(np.argmin(obsarray))
#         while rmin > mm * 1.1:
#             rmin -= 2.

#         mm = obsarray.max() + gobs.GetErrorYhigh(np.argmax(obsarray))
#         while rmax < mm * 1.1:
#             rmax += 2.

#     if int(rmax) % 10 == 0: # just to avoid axis label clashes
#         rmax -= 1.

#     canvas.yaxes[irow].SetNdivisions(405)
#     canvas.yaxes[irow].SetTitle('events / GeV')
#     canvas.raxes[irow].SetNdivisions(204)

#     for icol in range(ncol):
#         stack = stacks[icol]
#         signal = signals[icol]
#         uncert = uncerts[icol]
#         gobs = gobss[icol]

#         frame = uncert.Clone('frame')
#         _temporaries.append(frame)
#         frame.SetTitle('')
#         frame.Reset()
    
#         frame.SetTickLength(0.05, 'X')
#         frame.SetTickLength(0.03, 'Y')
#         frame.GetXaxis().SetNdivisions(canvas.xaxis.GetNdiv())
#         frame.GetXaxis().SetLabelSize(0.)
#         frame.GetXaxis().SetTitle('')
#         frame.GetYaxis().SetNdivisions(canvas.yaxes[irow].GetNdiv())
#         frame.GetYaxis().SetLabelSize(0.)
#         frame.SetMinimum(0.)
#         frame.SetMaximum(ymax * 1.4)

#         distpad = canvas.cd((irow * ncol + icol) * 2 + 1)
#         distpad.SetLogy(False)
#         distpad.SetTicky(1)
    
#         frame.Draw('HIST')
#         stack.Draw('SAME HIST')
#         uncert.Draw('SAME E2')
#         gobs.Draw('PZ')
    
#         distpad.Update()

#         runcert = uncert.Clone('runcert')
#         _temporaries.append(runcert)
    
#         bkg = rnp.hist2array(runcert)
#         bkg -= rnp.hist2array(signal, copy=False)
    
#         obsarray = rnp.array(ROOT.TArrayD(gobs.GetN(), gobs.GetY()))
#         obsarray -= bkg
    
#         robs = gobs.Clone('robs')
#         _temporaries.append(robs)
#         for ip in range(gobs.GetN()):
#             robs.SetPoint(ip, gobs.GetX()[ip], obsarray[ip])
    
#         rnp.array2hist(np.zeros_like(bkg), runcert)

#         rframe = frame.Clone('rframe')
#         _temporaries.append(rframe)
#         rframe.GetXaxis().SetTickLength(0.15)
#         rframe.GetYaxis().SetNdivisions(canvas.raxes[irow].GetNdiv())
#         rframe.SetMinimum(rmin)
#         rframe.SetMaximum(rmax)

#         ratiopad = canvas.cd((irow * ncol + icol) * 2 + 2)
#         ratiopad.SetLogy(False)
#         ratiopad.SetGridy(False)
#         ratiopad.SetTicky(1)

#         rframe.Draw('HIST')
#         runcert.Draw('SAME E2')
#         zero.DrawLine(rframe.GetXaxis().GetXmin(), 0., rframe.GetXaxis().GetXmax(), 0.)
#         signal.Draw('HIST SAME')
#         robs.Draw('PZ')
    
#         ratiopad.Update()

# ymax = 0.
# obsmax = max(mt_data[0].GetY()[ip] + mt_data[0].GetErrorYhigh(ip) for ip in range(mt_data[0].GetN()))
# uncmax = max(mt_stacks[0].GetMaximum() for ix in range(1, mt_sig[0].GetNbinsX() + 1))
# ymax = max(ymax, obsmax, uncmax)

# distpad = canvas.cd((1 * ncol + 1) * 2 + 1)
# distpad.SetLogy(False)
# distpad.SetTicky(1)


# frame = mt_sig[0].Clone('frame')
# _temporaries.append(frame)
# frame.SetTitle('')
# frame.Reset()


# frame.SetTickLength(0.05, 'X')
# frame.SetTickLength(0.03, 'Y')
# frame.GetXaxis().SetNdivisions(canvas.xaxis.GetNdiv())
# frame.GetXaxis().SetLabelSize(0.)
# frame.GetXaxis().SetTitle('')
# frame.GetYaxis().SetNdivisions(canvas.yaxes[1].GetNdiv())
# frame.GetYaxis().SetLabelSize(0.)
# frame.SetMinimum(0.)
# frame.SetMaximum(ymax * 1.4)



# frame.Draw('HIST')
# mt_stacks[0].Draw('SAME HIST')
# mt_stacks[0].Draw('SAME E2')
# mt_data[0].Draw('PZ')
        
# #distpad.Update()
# #runcert = uncert.Clone('runcert')
# #_temporaries.append(runcert)

# robs = mt_data[0].Clone('robs')
# _temporaries.append(robs)
# for ip in range(mt_data[0].GetN()):
#     print(mt_stacks[0].GetHistogram().GetBinContent(ip+1))
#     robs.SetPoint(ip, mt_data[0].GetX()[ip], mt_data[0].GetY()[ip] / mt_stacks[0].GetHistogram().GetBinContent(ip+1))
#     robs.SetPointError(ip, mt_data[0].GetErrorXlow()[ip], GetErrorXhigh()[ip], mt_data[0].GetErrorXlow()[ip] / mt_stacks[0].GetBinContent(ip+1), mt_data[0].GetErrorXhigh()[ip] / mt_stacks[0].GetBinContent(ip+1))

# print(robs.GetY())

# #tgrDataOverMC.SetPoint     (iBin, tgrData_vx[iBin], self.Ratio(tgrData_vy[iBin] , last.GetBinContent(iBin+1)) )
# #tgrDataOverMC.SetPointError(iBin, tgrData_evx[iBin], tgrData_evx[iBin], self.Ratio(tgrData_evy_do[iBin], last.GetBinContent(iBin+1)) , self.Ratio(tgrData_evy_up[iBin], last.GetBinContent(iBin+1)) )

# # rnp.array2hist(np.zeros_like(bkg), runcert)
            
            
# # rframe = frame.Clone('rframe')
# # _temporaries.append(rframe)
# # rframe.GetXaxis().SetTickLength(0.15)
# # rframe.GetYaxis().SetNdivisions(canvas.raxes[irow].GetNdiv())
# # rframe.SetMinimum(rmin)
# # rframe.SetMaximum(rmax)

# # ratiopad = canvas.cd((irow * ncol + icol) * 2 + 2)
# # ratiopad.SetLogy(False)
# # ratiopad.SetGridy(False)
# # ratiopad.SetTicky(1)

# # rframe.Draw('HIST')
# # runcert.Draw('SAME E2')
# # zero.DrawLine(rframe.GetXaxis().GetXmin(), 0., rframe.GetXaxis().GetXmax(), 0.)
# # signal.Draw('HIST SAME')
# # robs.Draw('PZ')

# # #        ratiopad.Update()


# # #tmpeps = '%s/tmp.eps' % os.getenv('TMPDIR')
# # #canvas.printout(tmpeps)
# # #_, err = subprocess.Popen(['gs', '-q', '-sDEVICE=bbox', '-dBATCH', '-dNOPAUSE', tmpeps], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
# # #for line in err.split('\n'):
# # #    if line.startswith('%%BoundingBox'):
# # #        words = line.split()
# # #        llx, lly, urx, ury = map(int, words[-4:])
# # #        width = urx + llx
# # #        height = ury + lly
# # #
# # #subprocess.Popen(['gs', '-q', '-o', '%s/postfit_sr_%s.pdf' % (args.out_path, args.observable), '-sDEVICE=pdfwrite', '-dPDFFitPage', '-g%d0x%d0' % (width, height), tmpeps]).communicate()
# # #os.unlink(tmpeps)
# # canvas.printout('%s/postfit_sr_%s.pdf' % (args.out_path, args.observable))
# # canvas.Print('%s/postfit_sr_%s.png' % (args.out_path, args.observable))






# #########################

# #print(tuple(mll[1:1 + 2]))
# #canvas.cd()
# #canvas.Draw()
# #canvas.SaveAs("test.png")
# c = ROOT.TCanvas("test","test", 800, 600)
# #mt_data[1].Draw()
# mt_stacks[0].Draw('HIST')
# mt_stacks[0].Draw('SAME nostack,e2')
# #c.cd()
# #mt_sigs[1].Draw()
# #histos_bkgs[0].GetXaxis().Set(5,mt);
# #histos_Others[0].Draw()
# #test.Draw()
# c.SaveAs("test.png")





