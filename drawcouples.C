//draw couples
void drawcouples(){
 bool dodraw=false;
 TString condition = TString("s.eMCEvt>=0"); //which segments to select
 const int ibrick = 5;
 TString runpath = TString(Form("/ship/DESY2019/RUN%i_sim/b00000%i/",ibrick,ibrick));

 const int nplates = 29;

 EdbVertexRec *gEVR = new EdbVertexRec();
 EdbCouplesTree *ect[nplates];
 EdbSegP *seg;

 //opening setfile (informations about transformations)
 TFile *setfile = TFile::Open((runpath+TString(Form("b00000%i.0.0.0.set.root",ibrick)).Data()));
 EdbScanSet *set = (EdbScanSet*) setfile->Get("set");

 TObjArray *sarr  = new TObjArray(); //array of segments to draw
 //starting from last plate
 
 float X, Y, Z; //segment positions
 float TX, TY; //segment angles
 float Prob; //segment probability
 
 //Defining histograms
 TH2D *hTXTY = new TH2D("hTXTY","Histogram for angles;TX;TY", 20,-0.05,0.05,20,-0.05,0.05);
 
 //************LOOP OVER PLATES************//
 for (int i = nplates; i >= 1; i--){ 
  //if(i==27 || i==20 || i== 6 || i==8) continue; // id of excluded plates
  //getting z position and affine transformation
  EdbPlateP* p = set->GetPlate(i);
  float zplate = p->Z();
  //if(!p) continue;
  EdbAffine2D *aff = new EdbAffine2D();
  set->GetAffP2P(i, nplates, *aff); //usually last plate is the reference one
  aff->Print();
  ect[i-1] = new EdbCouplesTree();
  //string spaghetti code
  if (i <10) ect[i-1]->InitCouplesTree("couples",(runpath+TString(Form("p00%i/%i.%i.0.0.cp.root",i,ibrick,i))).Data(),"READ");
  else ect[i-1]->InitCouplesTree("couples",(runpath+TString(Form("p0%i/%i.%i.0.0.cp.root",i,ibrick,i))).Data(),"READ");

  //loop into couples (only the ones passing condition)
  ect[i-1]->eTree->Draw(">>goodcouples", condition.Data());
  TEventList *goodcouples = (TEventList*) gDirectory->GetList()->FindObject("goodcouples");
  
  const int ngoodcouples = ect[i-1]->eTree->GetEntries(condition.Data());

  //int nseg = ect[i-1]->eTree->GetEntries();
  cout<<"Reading "<<ngoodcouples<<" from plate "<<i<<" at z position "<<zplate<<endl;
  //*************LOOP OVER SEGMENTS***************
  for (int iseg = 0; iseg< ngoodcouples; iseg++){
   //getting entry of good segment;
   int igoodsegment = goodcouples->GetEntry(iseg);
   //***Getting information about that segment***;
   ect[i-1]->GetEntry(igoodsegment);
   EdbSegP *seg = new EdbSegP();
   seg->Copy(*(ect[i-1]->eS));
   //setting z and affine transformation
   seg->SetZ(zplate);
   seg->SetDZ(300);
   seg->Transform(aff);
   
   //***Analysis of the segment***//
   //getting kinematic variables
   X = seg->X();
   Y = seg->Y();
   Z = seg->Z();
   TX = seg->TX();
   TY = seg->TY();
   //probability from fit
   Prob = seg->Prob();
   
   //***Filling histograms***//
   hTXTY->Fill(TX,TY);
   //add into the array of segments to draw   
   sarr->Add(seg);
  }
 }
 
 //DISPLAY OF SEGMENTS
 if(dodraw){
  const char *dsname = "DESY-testbeam-couples";
  ds = EdbDisplay::EdbDisplayExist(dsname);
  if(!ds)  ds=new EdbDisplay(dsname,-100000.,100000.,-100000.,100000.,-40000., 0..);
  ds->SetVerRec(gEVR);
  ds->SetDrawTracks(4);
  ds->SetArrSegP( sarr );
  ds->Draw();
 }
 
 TCanvas *c = new TCanvas();
 hTXTY->Draw("COLZ");
}
