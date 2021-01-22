void addbaricenter(){
    ROOT::RDataFrame df("treebranch","shower1.root");

    auto dfmean = df.Define("xmeanb","Mean(xb)")
                    .Define("ymeanb","Mean(yb)")
                    .Define("zmeanb","Mean(zb)");
    auto dfgoodshowers = dfmean.Filter("sizeb >= 50"); //selection by Maria

    auto hxymean = dfgoodshowers.Histo2D({"hxymean","Position of shower barycenter in transverse plane;x[#mum];y[#mum]", 
                                   125,0,125000,100,0,100000},{"xmeanb"},{"ymeanb"});

    auto hzmean = dfgoodshowers.Histo1D({"hzmean","Position of shower barycenter along beam;z[#mum]",
                                40,-40000,0},{"zmeanb"});

    auto hdxdy = dfgoodshowers.Define("dxmean","xb[0] - xmeanb;")
                              .Define("dymean","yb[0] - ymeanb;")
                              .Histo2D({"hdxdy","Difference between baricenter and fist segment;x[#mum];y[#mum]",
                               100,-500,500,100,-500,500},{"dxmean"},{"dymean"});                            

    TCanvas *xymean = new TCanvas();
    hxymean->SetMarkerStyle(kFullCircle);
    hxymean->SetMarkerColor(kRed);
    hxymean->DrawClone();

    TCanvas *zmean = new TCanvas();
    hzmean->DrawClone();

    TCanvas *cdxy = new TCanvas();
    hdxdy->SetMarkerStyle(kFullCircle);
    hdxdy->SetMarkerColor(kRed);
    hdxdy->DrawClone();
    
    dfmean.Snapshot("treebranch","shower1_barycenter.root",{"sizeb","xmeanb","ymeanb","zmeanb"});

}