using namespace ROOT;

RVec<float> barycenter_forplate(RVec<float> xb,RVec<int> plateb,int sizeb){
 //average position in each plate
 const int nplates = 29;

 RVec<float> xtotalplate[nplates]; //empty for all plates
 //RVec<int> sizebplate = RVec<int>(nplates); //how many for plate
 
 for (int isegment = 0; isegment < sizeb; isegment++){
  int whichplate = plateb[isegment];
  float x = xb[isegment];
  //increasing the number of segments and adding the position at this plate
  xtotalplate[whichplate].push_back(x);
 }

 RVec<float> xmeanbplate;
 for (int iplate = 0; iplate < nplates; iplate++){
     if (xtotalplate[iplate].size() > 0){ //store only plates where segments have been found
      xmeanbplate.push_back(Mean(xtotalplate[iplate]));
     }
 }
 //returning the array
 return xmeanbplate;
}

RVec<float> barycentererror_forplate(RVec<float> xb,RVec<int> plateb,int sizeb){
 //standard deviation of segments in each plate
 const int nplates = 29;

 RVec<float> xtotalplate[nplates]; //empty for all plates
 //RVec<int> sizebplate = RVec<int>(nplates); //how many for plate
 
 for (int isegment = 0; isegment < sizeb; isegment++){
  int whichplate = plateb[isegment];
  float x = xb[isegment];
  //increasing the number of segments and adding the position at this plate
  xtotalplate[whichplate].push_back(x);
 }

 RVec<float> xerrorplate;
 for (int iplate = 0; iplate < nplates; iplate++){
     if (xtotalplate[iplate].size() > 0){ //store only plates where segments have been found
      if (xtotalplate[iplate].size()>1){
       float stdeverror = StdDev(xtotalplate[iplate])/TMath::Sqrt(xtotalplate[iplate].size());
       if (stdeverror >= 0.){
       xerrorplate.push_back(stdeverror);
       }
       else xerrorplate.push_back(0.);
      }
      else
       xerrorplate.push_back(0.);
     }
 }
 return xerrorplate;
}

void addbaricenter(){
    RDataFrame df("treebranch","shower1.root");
    //storing RVec with positions separated for plate (max size 29)

    auto dfmeanplate = df.Define("xmeanplate",barycenter_forplate,{"xb","plateb","sizeb"})
                         .Define("ymeanplate",barycenter_forplate,{"yb","plateb","sizeb"})
                         .Define("zmeanplate",barycenter_forplate,{"zb","plateb","sizeb"});
    
    auto dfmeanplate_errors = dfmeanplate.Define("xmeanplate_error",barycentererror_forplate,{"xb","plateb","sizeb"})
                                         .Define("ymeanplate_error",barycentererror_forplate,{"yb","plateb","sizeb"})
                                         .Define("zmeanplate_error",barycentererror_forplate,{"zb","plateb","sizeb"});

    auto dfmean = dfmeanplate_errors.Define("xmean","Mean(xb)")
                                    .Define("ymean","Mean(yb)")
                                    .Define("zmean","Mean(zb)");
    //auto dfgoodshowers = dfmean.Filter("sizeb >= 50"); //selection by Maria
    auto dfgoodshowers = dfmean.Filter("1"); //no selection here, I want to keep all the showers

    auto hxymean = dfgoodshowers.Histo2D({"hxymean","Position of shower barycenter in transverse plane;x[#mum];y[#mum]", 
                                   125,0,125000,100,0,100000},{"xmean"},{"ymean"});

    auto hzmean = dfgoodshowers.Histo1D({"hzmean","Position of shower barycenter along beam;z[#mum]",
                                40,-40000,0},{"zmean"});

    auto hdxdy = dfgoodshowers.Define("dxmean","xb[0] - xmean;")
                              .Define("dymean","yb[0] - ymean;")
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
    
    dfmean.Snapshot("treebranch","shower1_barycenter.root",{"sizeb","xmean","ymean","zmean",
                                                            "xmeanplate","ymeanplate","zmeanplate",
                                                            "xmeanplate_error","ymeanplate_error","zmeanplate_error"});

}