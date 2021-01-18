//list of functions used for shower reconstruction from Maria dataset and efficiency estimation
//Created on 29 December 2020 by A.Iuliano
//Only thefirst time: launch countsignal_dataframe() to store number of initial signal and bacgkround from each event in a TTree
//Launch each shower reconstruction with doshowerrec()
//Evaluate efficiency and background rejections (Recalls for signal and background) with efficiency()
EdbPVRec* DataframePVRec_converter(){
    EdbPVRec *gAli = new EdbPVRec();

    auto buildsegment = [gAli] (Long64_t ID, Long64_t PID, double x, double y, double z, double TX, double TY, Long64_t MCEvent, Long64_t MCTrack,double P){
        EdbSegP seg(ID, x, y, TX, TY);
        seg.SetZ(z);
        seg.SetPID(PID);
        seg.SetPlate(29-PID); 
        seg.SetMC(MCEvent,MCTrack);
        seg.SetP(P);
        gAli->AddSegment(seg);
        return seg;
    };

    ROOT::RDataFrame df = ROOT::RDF::MakeCsvDataFrame("Final_dataset_RUN3_3.csv");
    auto colNames = df.GetColumnNames();
    // Print columns' names
    for (auto &&colName : colNames) std::cout << colName << std::endl;

    auto df0 = df.Define("Segment",buildsegment,{"ID","PID","x","y","z","TX","TY","MCEvent","MCTrack","P"});
    df0.Define("SegmentZ","Segment.Z()").Histo1D("SegmentZ")->DrawClone();
    return gAli;
}

EdbPVRec *GetInjectors(){
    EdbPVRec *gAli1 = new EdbPVRec();
    auto buildsegment = [gAli1] (Long64_t ID, Long64_t PID, double x, double y, double z, double TX, double TY, Long64_t MCEvent, Long64_t MCTrack,double P){
        EdbSegP seg(ID, x, y, TX, TY);
        seg.SetZ(z);
        seg.SetPID(PID);
        seg.SetPlate(29-PID); 
        seg.SetMC(MCEvent,MCTrack);
        seg.SetP(P);
        gAli1->AddSegment(seg);
        return seg;
    };

    ROOT::RDataFrame df = ROOT::RDF::MakeCsvDataFrame("Inizio_sciame_RUN3_3.csv");
    auto df0 = df.Define("Segment",buildsegment,{"ID","PID","x","y","z","TX","TY","MCEvent","MCTrack","P"});
    df0.Define("SegmentZ","Segment.Z()").Histo1D("SegmentZ")->DrawClone();
    return gAli1;
}

void doshowerreco(){

          double ConeRadius = 1000;
          double ConeAngle = 0.04;
          double ConnectionDR = 150;
          double ConnectionDT = 0.15;
          int NPropagation = 3;

          EdbShowerRec *eShowerRec = new EdbShowerRec();
          //Setting parameters
          eShowerRec->SetAlgoParameter(ConeRadius,0);
          eShowerRec->SetAlgoParameter(ConeAngle,1);
          eShowerRec->SetAlgoParameter(ConnectionDR,2);
          eShowerRec->SetAlgoParameter(ConnectionDT,3);
          eShowerRec->SetAlgoParameter(NPropagation,4);


               // Print parameters
          eShowerRec->PrintParameters();

    // Reset eShowerRec Arrays: InBTArray and RecoShowerArray....
          eShowerRec->ResetInBTArray();
          eShowerRec->ResetRecoShowerArray();
          // Create Initiator BT array:
          TObjArray * eInBTArray=new TObjArray();
          EdbPVRec *gAli1 = GetInjectors();

          int npatterns = gAli1->Npatterns();
          for (int ipattern = 0; ipattern < npatterns; ipattern++){
           int ninjectors = gAli1->GetPattern(ipattern)->N();
           for (int iseg = 0; iseg < ninjectors; iseg++){
              eInBTArray->Add(gAli1->GetPattern(ipattern)->GetSegment(iseg));
           }
          }          
          eShowerRec->SetInBTArray(eInBTArray);
          eShowerRec->PrintInitiatorBTs();

          //set edbpvrec, need to add a segment to the other pvrec?
          EdbPVRec* gAli = DataframePVRec_converter();
          //EdbSegP *exampleseg = (EdbSegP*) segarray->At(0);
          //gAli->AddSegment(*exampleseg);

          EdbPattern *firstplate = new EdbPattern();
          firstplate->SetZ(-36820.0);
          gAli->AddPattern(firstplate);

          for(int i=0; i<29; i++) {
              if(gAli->GetPattern(i)) gAli->GetPattern(i)->SetPID(29-i);

          }
          eShowerRec->SetEdbPVRec(gAli);

          cout << " eShowerRec->SetUseAliSub(0)..." << endl;
          eShowerRec->SetUseAliSub(0);

          cout << " eShowerRec->Execute()..." << endl;

          //Start actual reconstruction
          eShowerRec->Execute();

          //Print output
          eShowerRec->PrintRecoShowerArray();
}

void countsignal_dataframe(){
    //saving a tree file with nsignal and nbackground for each event, denominators for efficiency estimation
    //in Maria's dataset she kept conting events from previous datasets, this then does not start from 0
    ROOT::RDataFrame df = ROOT::RDF::MakeCsvDataFrame("Final_dataset_RUN3_3.csv");
    const int startshowerevent = 720;
    const int endshowerevent = 1080;
    const int ntotalshowers = endshowerevent - startshowerevent;
    //preparing outputtree
    int MCEventID, nsignal, nbackground;
    TFile *outputfile = new TFile("Final_dataset_RUN3_3_nsigbkg.root","RECREATE");
    TTree *expectedshowers = new TTree("expectedshowers","Signal and background in each shower provided by Maria");
    expectedshowers->Branch("MCEventID",&MCEventID, "MCEventID/I");
    expectedshowers->Branch("nsignal",&nsignal,"nsignal/I");
    expectedshowers->Branch("nbackground",&nbackground,"nbackground/I");
    //loop over all reconstructed showers, counting signal and background
    cout<<"Total number of showers "<< ntotalshowers<<endl;
    for (int ishower = startshowerevent; ishower < startshowerevent + ntotalshowers; ishower++){
      MCEventID = ishower;
      cout<<"Arrived at shower "<<MCEventID<<endl;
      //getting the input dataframe for that event
      auto df0 = df.Filter(Form("Ishower==%i",MCEventID));
      auto nsignaldf = df0.Filter("Signal==1").Count();
      auto nbackgrounddf = df0.Filter("Signal==0").Count();
      //RDataframe store counters in pointers, need to access values to store them inside the TTree.
      nsignal = *nsignaldf;
      nbackground = *nbackgrounddf;
      //filling shower, going to next one
      expectedshowers->Fill();
    }
    //end of loop, writing output
    outputfile->cd();
    expectedshowers->Write();
    outputfile->Close();

}

vector<double> eff_formula(int foundevents, int totalevents){
  vector<double> efficiency; //value and error
  
  efficiency.push_back((double) foundevents/totalevents);

  //totalweight and foundweight are weighted, I need to divide with the actual number of events simulated!
  double efferr = TMath::Sqrt(efficiency[0] * (1- efficiency[0])/totalevents);
  efficiency.push_back(efferr);
  
  return efficiency;
}

void efficiency(TString foldername = "dR250"){
  //in Maria's dataset she kept conting events from previous datasets, this then does not start from 0
  const int startshowerevent = 720;
  const int endshowerevent = 1080;
  const int ntotalshowers = endshowerevent - startshowerevent;
  //total signal and background from ttree
  TFile *inputfile = TFile::Open("Final_dataset_RUN3_3_nsigbkg.root");
  TTree *expectedshowers = (TTree*) inputfile->Get("expectedshowers");
  int nsignal, nbackground;
  //build index with event
  expectedshowers->BuildIndex("MCEventID");
  //set  addresses
  expectedshowers->SetBranchAddress("nsignal",&nsignal);
  expectedshowers->SetBranchAddress("nbackground",&nbackground);
  
  //loop over all reconstructed showers, evaluating efficiencies
  TFile *showerfile = TFile::Open(foldername+"/shower1.root");
  TTree *treebranch = (TTree*) showerfile->Get("treebranch");

  //set branches
  const int maxsize = 1000;
  int sizeb, MCEvents[maxsize];
  treebranch->SetBranchAddress("sizeb", &sizeb);
  treebranch->SetBranchAddress("ntrace1simub",&MCEvents);

  int nshowers = treebranch->GetEntries();

  //histograms to be filled
  TH1F *heff = new TH1F("heff","Efficiency",25,0,1);
  TH1F *hbakrej = new TH1F("hbakrej","Background rejction",25,0,1);
  TH1F *hpurity = new TH1F("hpurity","Purity",25,0,1);
  TH1F *hfscore = new TH1F("hfscore","F-Score",25,0,1);

  //total counters (over all showers)
  int ntotsignalselected = 0;
  int ntotbackgroundselected = 0;
  int ntotsignal = 0;
  int ntotbackground = 0;
  //start main loop 
  treebranch->BuildIndex("ntrace1simub[0]");
  cout<<"Stored showers "<<nshowers<<" over "<< ntotalshowers<<endl;

  fstream performancefile("performance_standardreco.csv",fstream::out);
  performancefile<<"MCEventID,Recall,Precision,Fscore"<<endl;
  for (int MCEventID = startshowerevent; MCEventID < startshowerevent + ntotalshowers; MCEventID++){
      int nsignalselected = 0;
      int nbackgroundselected = 0;
      int showerindex = treebranch->GetEntryNumberWithIndex(MCEventID);
      if (showerindex >= 0){
       treebranch->GetEntry(showerindex);       
       //loop over shower segments, how many from the same event as injector? 
       //(n.d.r I start from second segment, first is injector)
       for (int isegment = 1; isegment < sizeb; isegment++){
          if (MCEvents[isegment] == MCEventID) nsignalselected++;
          else nbackgroundselected++;
       }
      }
      //getting the input dataframe for that event
      int ishower = expectedshowers->GetEntryNumberWithIndex(MCEventID);
      if (ishower >= 0) expectedshowers->GetEntry(ishower);
      else cout<<"ERROR: not found entry with tot signal and background! Check input file"<<endl;

      //filling efficiency/purity histograms
      double efficiency = (double) nsignalselected/ nsignal;
      double backgroundrej = 1. - (double) nbackgroundselected/ nbackground;

      heff->Fill(efficiency);
      hbakrej->Fill(backgroundrej);

      double purity;

      //purity has not sense if shower is not found
      if (showerindex >= 0){
          purity = (double) nsignalselected/sizeb;
      }
      else{
          purity = 0.;
      } 
      hpurity->Fill(purity);

      double fscore = 2*efficiency*purity/(efficiency+purity);
      if (efficiency == 0. && purity == 0.) fscore = 0.;
      hfscore->Fill(fscore);
      performancefile << MCEventID<<","<<efficiency << "," << purity << "," << fscore<< endl;


      //increasing total counters and moving to next event
      ntotsignal += nsignal;
      ntotbackground += nbackground;
      ntotsignalselected += nsignalselected;
      ntotbackgroundselected += nbackgroundselected;
  }
  cout<<"End of loop, priting results "<<endl;
 
  vector<double> efficiency = eff_formula(ntotsignalselected, ntotsignal);
  vector<double> backgroundrej = eff_formula(ntotbackground - ntotbackgroundselected, ntotbackground);
  vector<double> purity = eff_formula(ntotsignalselected,ntotsignalselected + ntotbackgroundselected);
 
  cout<<"Efficiency (1->1): "<<efficiency[0]<<" with error "<<efficiency[1]<<endl;
  cout<<"Background rejection (2->2): "<<backgroundrej[0]<<" with error "<<backgroundrej[1]<<endl;
  cout<<"Purity (nsignalfound/nallfound): "<<purity[0]<<" with error "<<purity[1]<<endl;

  TCanvas *ceff = new TCanvas();
  heff->Draw();
  TCanvas *cbakrej = new TCanvas();
  hbakrej->Draw();
  TCanvas *cpurity = new TCanvas();
  hpurity->Draw();
  TCanvas *cfscore = new TCanvas();
  hfscore->Draw();

  double meaneff = heff->GetMean();
  double meanpurity = hpurity->GetMean();
  double meanfscore = hfscore->GetMean();

  double erreff = heff->GetStdDev()/TMath::Sqrt(heff->GetEntries());
  double errpurity = hpurity->GetStdDev()/TMath::Sqrt(hpurity->GetEntries());
  double errfscore = hfscore->GetStdDev()/TMath::Sqrt(hfscore->GetEntries());

  cout<<"Mean efficiency "<<meaneff <<" with error"<<erreff<<endl;
  cout<<"Mean purity "<<meanpurity <<" with error"<<errpurity<<endl;
  cout<<"Mean fscore "<<meanfscore<<" with error"<<errfscore<<endl;

  performancefile.close();
}

void drawefficiencies(){
   //draw efficiencies stored in tables (X Y EY)
   //from input file, format "%lg %lg %lg" for no error in x, see ROOT TGraphError reference
   TGraphErrors * effgraph = new TGraphErrors("eff_table.dat","%lg %lg %lg"); 
   TGraphErrors * bkgrejgraph = new TGraphErrors("bkgrej_table.dat","%lg %lg %lg");
   TGraphErrors * puritygraph = new TGraphErrors("purity_table.dat","%lg %lg %lg");

   TCanvas *graphs = new TCanvas();
   effgraph->SetTitle("Efficiency;dR[#mum];%");
   effgraph->SetMarkerColor(kRed);
   effgraph->SetMarkerStyle(kFullCircle);
   effgraph->GetYaxis()->SetRangeUser(0,100);
   effgraph->Draw("AP");

   bkgrejgraph->SetTitle("Background Rejection");
   bkgrejgraph->SetMarkerColor(kBlue);
   bkgrejgraph->SetMarkerStyle(kFullStar);
   bkgrejgraph->Draw("P");
   
   puritygraph->SetTitle("Purity");
   puritygraph->SetMarkerColor(kBlack);
   puritygraph->SetMarkerStyle(kFullSquare);
   puritygraph->Draw("P");

   graphs->BuildLegend();

}