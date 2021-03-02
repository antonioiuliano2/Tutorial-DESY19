'''fitting shower barycenter per plate'''
import ROOT as r
import os

hslopezx = r.TH1D("hslopezx","Slope of fit with zx;slope",200,-1,1)
hslopezy = r.TH1D("hslopezy","Slope of fit with zy;slope",200,-1,1)

def dofits():
 #reproducing trees for safety
 os.system('root -l -q /home/utente/Lavoro/Tutorial-DESY19/shower_reconstruction/addbaricenter.C')

 print("END OF C++ code, starting fit")
 showerfile = r.TFile.Open("shower1_barycenter.root")
 showertree = showerfile.Get("treebranch")

 showerchain = r.TChain("treebranch")

 #"/home/utente/Lavoro/DE19_R7/recoshower_5_December_2020"
 #"/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11"

 outputfile = r.TFile("shower1_fitresults.root","RECREATE")

 #loop over showers
 for ishower,shower in enumerate(showertree):
  graphzx = r.TGraphErrors()
  graphzy = r.TGraphErrors()
  graphzx.SetName("graphzx_{}".format(ishower))
  graphzy.SetName("graphzy_{}".format(ishower))
  #giving title
  graphzx.SetTitle("zx distribution of shower barycenters per plate for shower {};z[#mum];x[#mum]".format(ishower))
  graphzy.SetTitle("zy distribution of shower barycenters per plate for shower {};z[#mum];y[#mum]".format(ishower))

  fzx = r.TF1("fzx_{}".format(ishower),"pol1",-40000,0)
  fzy = r.TF1("fzy_{}".format(ishower),"pol1",-40000,0)

  xmeanplate = shower.xmeanplate
  ymeanplate = shower.ymeanplate
  zmeanplate = shower.zmeanplate
  xerrorplate = shower.xmeanplate_error
  yerrorplate = shower.ymeanplate_error 
  zerrorplate = shower.zmeanplate_error
  #adding points to graphs
  for ipoint,(x,y,z,xerror,yerror,zerror) in enumerate(zip(xmeanplate,ymeanplate,zmeanplate,
                                                          xerrorplate,yerrorplate,zerrorplate)):
   graphzx.SetPoint(ipoint,z,x)
   graphzy.SetPoint(ipoint,z,y)
    
   graphzx.SetPointError(ipoint,0.,xerror)
   graphzy.SetPointError(ipoint,0.,yerror)

  #performing the fits and saving the results, along with the graph
  graphzx.Fit(fzx,"W") #ignore point errors during fit
  graphzy.Fit(fzy,"W")

  graphzx.Write()
  graphzy.Write()

 outputfile.Close()

def readfitresults():
    '''read fit result for each shower, select according to shower size'''
    showerfile = r.TFile.Open("shower1.root")
    showertree = showerfile.Get("treebranch")

    #read file with graphs
    fitfile = r.TFile.Open("shower1_fitresults.root")

    minsize = 50

    clineszx = r.TCanvas()
    clineszy = r.TCanvas()
    first = True
    #start loop on showers
    for ishower, shower in enumerate(showertree):
        size = shower.sizeb
        if(size >= minsize):
            graphzx = fitfile.Get("graphzx_{}".format(ishower))
            graphzy = fitfile.Get("graphzy_{}".format(ishower))
            #getting fitted function
            fzx = graphzx.GetFunction("fzx_{}".format(ishower))
            fzy = graphzy.GetFunction("fzy_{}".format(ishower))

            #if they are found, fill histograms
            if (fzx):
                hslopezx.Fill(fzx.GetParameter(1))
            if (fzy):
                hslopezy.Fill(fzy.GetParameter(1))
            
            fzx.SetParameter(0,50000)
            fzy.SetParameter(0,50000)
            #first time, drawing without same and setting title
            if (first):
             first = False
             clineszx.cd()
             fzx.SetTitle("Line bundle in zx plane;z[#mum];x[#mum]")
             fzx.Draw()
             fzx.GetYaxis().SetRangeUser(49000,50200)
             clineszy.cd()
             fzy.SetTitle("Line bundle in zy plane;z[#mum];y[#mum]")
             fzy.Draw()
             fzy.GetYaxis().SetRangeUser(49500,50500)
            else:
             clineszx.cd()
             fzx.Draw("SAME")
             clineszy.cd()
             fzy.Draw("SAME")
    clineszx.Print("fasciozx.png")
    clineszy.Print("fasciozy.png")

#what do we do now?
#dofits()

readfitresults()

czx = r.TCanvas()
hslopezx.Draw()

czy = r.TCanvas()
hslopezy.Draw()