//code to read shower tree and inspect developmentin x0 units (created 27 November 2020)
//nplates: number of PASSIVE plates (i.e. 28 for RUN3)
void depth_shower(int nplates){
 //accessing shower file
    TFile *showerfile = TFile::Open("shower1.root");
    TTree *showertree = (TTree*) showerfile->Get("treebranch");

    const int material = 1;//0 is lead, 1 is W
    //numerical constants, from PDG
    const float radlen[2] = {5.612 , 3.504}; //in mm, from PDG https://pdg.lbl.gov/2020/AtomicNuclearProperties/
    const float dzpassive[2] = {1.0, 0.9}; //passive block thickness, tunsgten ones are smaller

    const int nshowers = showertree->GetEntries();
    const int minsize = 60; //to consider it a "good" shower

    int sizeb; 
    const int maxsize = 10000; //as in ShowerRec
    int idb[maxsize]; //IDs of basetracks
    int plateb[maxsize]; //number of plate of base track
    float xb[maxsize],yb[maxsize],zb[maxsize],txb[maxsize],tyb[maxsize]; //position and angles

    //setting branch addresses
    showertree->SetBranchAddress("sizeb",&sizeb);
    showertree->SetBranchAddress("idb",&idb);
    showertree->SetBranchAddress("plateb",&plateb);
    showertree->SetBranchAddress("xb",&xb);
    showertree->SetBranchAddress("yb",&yb);
    showertree->SetBranchAddress("zb",&zb);
    showertree->SetBranchAddress("txb",&txb);
    showertree->SetBranchAddress("tyb",&tyb);

    TH1I *hsize = new TH1I("hsize","Size of shower;sizeb",25,0,250);

    TH1F *hdepth = new TH1F("hdepth", "Shower development;#X0;fraction of segments",600,0,6);

    cout<<"Starting loop assuming number of passive plates "<<nplates <<" and material (0:Pb, 1:W) "<<material<<endl;

    //******************START OF MAIN LOOP WITHIN SHOWERS**********
    for (int ishower = 0; ishower < nshowers; ishower++){

     showertree->GetEntry(ishower);
     hsize->Fill(sizeb);
     //loop on shower segments
     for (int iseg = 0; iseg < sizeb; iseg++){
       float depth = ((nplates - plateb[iseg]) * dzpassive[material])/radlen[material];
       
       if (sizeb >= minsize) hdepth->Fill(depth);
     }

    }
  //********************END OF LOOP, DRAWING PLOTS************
  TCanvas *csize = new TCanvas();
  hsize->Draw();

  TCanvas *cdepth = new TCanvas();
  hdepth->Sumw2();
  hdepth->Scale(1./hdepth->Integral()); //normalizing depth to number of segments
  hdepth->Draw("E");

    
}
