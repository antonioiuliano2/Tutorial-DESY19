import ROOT as r

#getting ml dataframe
mariadf = r.RDF.MakeCsvDataFrame("Lunghezza_sciame_pred_new.csv")

#getting ml precision and recall histograms

hmlprecision = mariadf.Histo1D(("hmlprecision","Precision from Random Forest;Precision",25,0,1),"Precision")
hmlrecall = mariadf.Histo1D(("hmlrecall","Recall from Random Forest;Recall",25,0,1),"Recall")
hmlfscore = mariadf.Histo1D(("hmlfscore","F_score from Random Forest;F_score",25,0,1),"F_score")

#standardf = r.RDF.MakeCsvDataFrame("performance_standard_reco.csv")
#hstandardprecision = standardf.Histo1D(("hstandardprecision","Precision from standard reconstruction;Precision",25,0,1),"Precision")
#hstandardrecall = standardf.Histo1D(("hstandardrecall","Recall from standard reconstruction;Recall",25,0,1),"Recall")
#hstandardfscore = standardf.Histo1D(("hstandarddf","F_score from standard reconstruction;F_score",25,0,1),"F_score")

#getting standard precision and recall histograms

standardfile = r.TFile.Open("performance_standard_reco.root")

hstandardprecision = standardfile.Get("c1_n3").GetPrimitive("hpurity")
hstandardprecision.SetTitle("Precision from standard reconstruction;Precision")
hstandardrecall = standardfile.Get("c1").GetPrimitive("heff")
hstandardrecall.SetTitle("Recall from standard reconstruction;Recall")
hstandardfscore = standardfile.Get("c1_n4").GetPrimitive("hfscore")
hstandardfscore.SetTitle("F_score from standard reconstruction;F_score")

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

cfscore = r.TCanvas()
hmlfscore.DrawClone()
hstandardfscore.SetLineColor(r.kRed)
hstandardfscore.Draw("SAMES")
cfscore.BuildLegend()

