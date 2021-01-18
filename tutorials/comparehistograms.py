import ROOT as r

#getting ml dataframe
mariadf = r.RDF.MakeCsvDataFrame("Lunghezza_sciame_pred_new.csv")

#getting ml precision and recall histograms

hmlprecision = mariadf.Histo1D(("hmlprecision","Precision from Random Forest;Precision",25,0,1),"Precision")
hmlrecall = mariadf.Histo1D(("hmlrecall","Recall from Random Forest;Recall",25,0,1),"Recall")

#getting standard precision and recall histograms

precisionfile = r.TFile.Open("purity_standard_reco.root")
recallfile = r.TFile.Open("efficiency_standard_reco.root")

hstandardprecision = precisionfile.Get("c1_n3").GetPrimitive("hpurity")
hstandardprecision.SetTitle("Precision from standard reconstruction;Precision")
hstandardrecall = recallfile.Get("c1").GetPrimitive("heff")
hstandardrecall.SetTitle("Recall from standard reconstruction;Recall")

#drawing histograms with legend
cprecision = r.TCanvas()
hmlprecision.DrawClone() #RDataFrame object need DrawClone(), not Draw(). They are "lazy", do not exist until now
hstandardprecision.SetLineColor(r.kRed)
hstandardprecision.Draw("SAMES")
cprecision.BuildLegend()

crecall = r.TCanvas()
hmlrecall.DrawClone()
hstandardrecall.SetLineColor(r.kRed)
hstandardrecall.Draw("SAMES")
crecall.BuildLegend()

