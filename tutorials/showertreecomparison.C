//opening a ROOT RDataFrame with a shower and computing topological variables (IP, etc. A. Iuliano 19 Feb 2021)
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
    txproj = Take(txproj, txproj.size()-1);
    typroj = Take(typroj, typroj.size()-1);

    RVec<float> thetaproj = sqrt((txproj - txb[0]) * (txproj - txb[0]) + (typroj - tyb[0]) * (typroj - tyb[0])); //first segment is the vertex

    return atan(thetaproj);
}
ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> showerdataframe(TString filepath){
 RDataFrame df("treebranch",filepath.Data());
 auto df0 = df.Filter("sizeb>=50"); //selection!

 auto df1 = df0.Define("dz","zb - zb[0]");
 auto df2 = df1.Define("IP",calcIP,{"dz","xb","yb","txb","tyb"});
 
//Take is needed to exclude the vertex (it takes the last size -1 segments)
 auto df3 = df2.Define("normIP","Take(IP/dz,IP.size()-1)"); 

 auto df4 = df3.Define("thetaproj",calcthetaproj,{"dz","xb","yb","txb","tyb"});

 return df4;


}

void showertreecomparison(){
    auto datadf = showerdataframe("/eos/experiment/ship/data/DESY19TB/DE19_R7/recoshower_5_December_2020/shower1.root");
    auto simdf = showerdataframe("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN7_28_December_2020/b000007/shower1.root");

    auto hdata_IP = datadf.Histo1D({"hdata_IP","Data;IP/#DeltaZ",30,0.,0.3},"normIP");
    auto hdata_thetaproj = datadf.Histo1D({"hdata_thetaproj","Data;#theta'_{bt}[rad]",50,0,0.05},"thetaproj");

    auto hsim_IP = simdf.Histo1D({"hsim_IP","Simulation;IP/#DeltaZ",30,0.,0.3},"normIP");
    auto hsim_thetaproj = simdf.Histo1D({"hsim_thetaproj","Simulation;#theta'_{bt}[rad]",50,0,0.05},"thetaproj");

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
}
