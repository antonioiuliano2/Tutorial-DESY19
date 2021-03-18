/*opening a ROOT RDataFrame with a shower and computing topological variables (IP, etc. A. Iuliano 19 Feb 2021)
adding function to compare histograms with Random Forest results 
(saved in ROOT file with Make_histograms_data.py), launch RMcomparison*/
using namespace ROOT;
RVec<float> calcIP(RVec<float> dz, RVec<float> xb, RVec<float> yb, RVec<float> txb, RVec<float>tyb){
    //compute IP to vertex
    RVec<float> xproj = xb - txb * dz;
    RVec<float> yproj = yb - tyb * dz;

    RVec<float> IP = sqrt(pow(xproj - xb[0],2) + pow(yproj - yb[0],2)); //first segment is the vertex
    return IP;
}

RVec<float> calcthetaproj(RVec<float> dz, RVec<float>xb, RVec<float>yb, RVec<float> txb, RVec<float> tyb){
    RVec<float> txproj = (xb - xb[0])/dz; // projections
    RVec<float> typroj = (yb - yb[0])/dz;
    txproj = Take(txproj, -(txproj.size()-1));
    typroj = Take(typroj, -(typroj.size()-1));

    RVec<float> thetaproj = sqrt((txproj - txb[0]) * (txproj - txb[0]) + (typroj - tyb[0]) * (typroj - tyb[0])); //first segment is the vertex

    return atan(thetaproj);
}
ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> showerdataframe(TString filepath){
 RDataFrame df("treebranch",filepath.Data());
 auto df0 = df.Filter("sizeb>=50"); //selection!

 auto df1 = df0.Define("dz","zb - zb[0]");
 auto df2 = df1.Define("IP",calcIP,{"dz","xb","yb","txb","tyb"});
 
//Take is needed to exclude the vertex (it takes the last size -1 segments)
 auto df3 = df2.Define("normIP","Take(IP/dz,-(IP.size()-1))"); 

 auto df4 = df3.Define("thetaproj",calcthetaproj,{"dz","xb","yb","txb","tyb"});

 auto df5 = df4.Define("zbnofirst","Take(zb,-(zb.size()-1))");

 return df5;


}

void showertreecomparison(){
    //auto datadf = showerdataframe("/eos/experiment/ship/data/DESY19TB/DE19_R7/recoshower_5_December_2020/shower1.root");
    //auto simdf = showerdataframe("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN7_28_December_2020/b000007/shower1.root");
    TFile *datahistofile = new TFile("/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11/RUN3_standardrecohistos.root","RECREATE");

    auto datadf = showerdataframe("/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11/shower1.root");
    auto simdf = showerdataframe("/home/utente/Simulations/RUN3_uniform_26_July_2020/b000003/recoshowers/radius1000alpha0.04/shower1.root");

    auto hdata_IP = datadf.Histo1D({"hdata_IP","Data;IP/#DeltaZ",30,0.,0.3},"normIP");
    auto hdata_thetaproj = datadf.Histo1D({"hdata_thetaproj","Data;#theta'_{bt}[rad]",40,0,0.04},"thetaproj");

    auto hdata2D_IP = datadf.Histo2D({"hdata2D_IP","Data;z[#mum];IP/#DeltaZ",40,-40000.,0.1,30,0.,0.3},"zbnofirst","normIP");
    auto hdata2D_thetaproj = datadf.Histo2D({"hdata2D_thetaproj","Data;z[#mum];#theta'_{bt}[rad]",40,-40000.,0.1,40,0,0.04},"zbnofirst","thetaproj");

    auto hsim_IP = simdf.Histo1D({"hsim_IP","Simulation;IP/#DeltaZ",30,0.,0.3},"normIP");
    auto hsim_thetaproj = simdf.Histo1D({"hsim_thetaproj","Simulation;#theta'_{bt}[rad]",40,0,0.04},"thetaproj");

    auto hsim2D_IP = simdf.Histo2D({"hsim2D_IP","Sim;z[#mum];IP/#DeltaZ",40,-40000.,0.1,30,0.,0.3},"zbnofirst","normIP");
    auto hsim2D_thetaproj = simdf.Histo2D({"hsim_thetaproj","Sim;z[#mum];#theta'_{bt}[rad]",40,-40000.,0.1,40,0,0.04},"zbnofirst","thetaproj");

    //drawing histograms
    TCanvas *c0 = new TCanvas();
    hdata_IP->Scale(1/hdata_IP->Integral());
    hsim_IP->Scale(1/hsim_IP->Integral());
    hsim_IP->SetLineColor(kRed);
    hsim_IP->DrawClone("histo");
    hdata_IP->DrawClone("SAMES&&histo");
    c0->BuildLegend();

    TCanvas *c1 = new TCanvas();
    hdata_thetaproj->Scale(1/hdata_thetaproj->Integral());
    hsim_thetaproj->Scale(1/hsim_thetaproj->Integral());
    hsim_thetaproj->SetLineColor(kRed);
    hsim_thetaproj->DrawClone("histo");
    hdata_thetaproj->DrawClone("SAMES&&histo");
    c1->BuildLegend();

    //adding full size
    RDataFrame fulldatadf("treebranch","/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11/shower1.root");
    auto hdata_size = fulldatadf.Histo1D({"hdata_size","Shower size;Nsegments",18,0,180},"sizeb");
    TCanvas *csize = new TCanvas();
    hdata_size->DrawClone();

    TCanvas *c2Dip = new TCanvas();
    c2Dip->Divide(1,2);
    c2Dip->cd(1);
    hdata2D_IP->DrawClone("COLZ");
    c2Dip->cd(2);
    hsim2D_IP->DrawClone("COLZ");

    TCanvas *c2Dthetaproj = new TCanvas();
    c2Dthetaproj->Divide(1,2);
    c2Dthetaproj->cd(1);
    hdata2D_thetaproj->DrawClone("COLZ");
    c2Dthetaproj->cd(2);
    hsim2D_thetaproj->DrawClone("COLZ");

    //writing histograms to file
    datahistofile->cd();
    hdata_IP->Write();
    hdata_thetaproj->Write();
    hdata_size->Write();

}

void PrepareHistogram(TH1D* histo, const char * name, const char* title, int linecolor){

    histo->Scale(1./histo->Integral());
    histo->SetName(name);
    histo->SetTitle(title);
    histo->SetLineColor(linecolor);

}

void RMcomparison(){
    TFile *standardrecofile = TFile::Open("/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11/RUN3_standardrecohistos.root");
    TFile *RandomForestfile = TFile::Open("/home/utente/Lavoro/DE19_R3/RUN3_RandomForest_histos.root");
    
    //getting standard reco histograms
    TH1D* hstandard_size = (TH1D*) standardrecofile->Get("hdata_size");
    PrepareHistogram(hstandard_size,"hstandard_size","Standard Reconstruction;NSegments",kBlue);
    TH1D* hstandard_normIP = (TH1D*) standardrecofile->Get("hdata_IP");
    PrepareHistogram(hstandard_normIP,"hstandard_normIP","Standard Reconstruction;IP/#DeltaZ",kBlue);
    TH1D* hstandard_thetaproj = (TH1D*) standardrecofile->Get("hdata_thetaproj");
    PrepareHistogram(hstandard_thetaproj,"hstandard_thetaproj","Standard Reconstruction;#theta'",kBlue);

    //getting Random Forest reco histograms
    TH1D* hRM_size = (TH1D*) RandomForestfile->Get("hsizeML");
    PrepareHistogram(hRM_size,"hRM_size","Random Forest Reconstruction;NSegments",kRed);
    TH1D* hRM_normIP = (TH1D*) RandomForestfile->Get("hIPnorm");
    PrepareHistogram(hRM_normIP,"hRM_normIP","Random Forest Reconstruction;IP/#DeltaZ",kRed);
    TH1D* hRM_thetaproj = (TH1D*) RandomForestfile->Get("hthetaprime");
    PrepareHistogram(hRM_thetaproj,"hRM_thetaproj","Random Forest Reconstruction;#theta'",kRed);

    TCanvas *csize = new TCanvas();
    hstandard_size->Draw("histo");
    hRM_size->Draw("histo && SAMES");
    csize->BuildLegend();
    hstandard_size->SetTitle("Size of reconstructed showers;NSegments");

    TCanvas *cnormIP = new TCanvas();
    hstandard_normIP->Draw("histo");
    hRM_normIP->Draw("histo && SAMES");
    cnormIP->BuildLegend();
    hstandard_normIP->SetTitle("Impact parameter over distance along axis;IP/#DeltaZ");

    TCanvas *cthetaproj = new TCanvas();
    hstandard_thetaproj->Draw("histo");
    hRM_thetaproj->Draw("histo && SAMES");
    cthetaproj->BuildLegend();
    hstandard_thetaproj->SetTitle("Cone angle with respect to shower start;#theta'[rad]");
}