'''fitting shower barycenter per plate'''
import ROOT as r
import os
#reproducing trees for safety
os.system('root -l -q /home/utente/Lavoro/Tutorial-DESY19/shower_reconstruction/addbaricenter.C')

print("END OF C++ code, starting fit")
showerfile = r.TFile.Open("shower1_barycenter.root")
showertree = showerfile.Get("treebranch")

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
 graphzx.Fit(fzx)
 graphzy.Fit(fzy)

 graphzx.Write()
 graphzy.Write()

outputfile.Close()