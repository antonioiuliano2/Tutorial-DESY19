/*simple script to loop over events, MC tracks and hit points
Works without any include, provided that we are in FairShip environment,
just launch root -l simple_loop in the folder with the simulation output*/
void desyshowerloop(TString filename = "ship.conical.PG_11-TGeant4.root"){

 TFile *file = TFile::Open(filename.Data(),"READ"); 
 if (!file) return;
 TTreeReader reader("cbmsim",file);

 TTreeReaderArray<ShipMCTrack> tracks(reader,"MCTrack");
 TTreeReaderArray<EmuDESYPoint> emupoints(reader,"EmuDESYPoint");

 TDatabasePDG *pdg = TDatabasePDG::Instance();

 int nplates = 57;

// cout<<"Number of events"<<reader.GetEntries()<<endl;
 int ientry = 0;
 int pdgcode,plateid;
 double mass, charge,momentum, energy;

 TProfile * hE_pid = new TProfile("hE_pid","Energy vs PID;PID;E[GeV]", nplates,1,nplates+1, 0, 400);
 TH1I *hoccupancy = new TH1I("hoccupancy","Number of particles per plate", nplates,1, nplates+1);
 TH1D *hmaxplate = new TH1D("hmaxplate","plate with maximum number of particles;PID",nplates,1,nplates+1);

 TH1D *hmaxsegments = new TH1D("hmaxsegments","number of segments at maximum;nelectrons",100,0,100);

 const int nevents = reader.GetEntries();
 
 cout<<"Starting loop over "<<nevents<<endl;

 int nelectrons[nplates];
 int maxelectrons;
 int maxplate;
 for(int ievent = 0; ievent<nevents;ievent++){
     for(int iplate =0; iplate < nplates; iplate++){
      nelectrons[iplate] = 0; //resetting number of electrons;
     }

     reader.SetEntry(ievent);
     //access the hits:    
     for (const EmuDESYPoint& emupoint: emupoints){
         //pdgcode and kinematics
         pdgcode = emupoint.PdgCode();
         momentum = TMath::Sqrt(pow(emupoint.GetPx(),2) + pow(emupoint.GetPy(),2) + pow(emupoint.GetPz(),2));
         plateid = emupoint.GetDetectorID();
         //checking particle information
         if(pdg->GetParticle(pdgcode)){
          charge = pdg->GetParticle(pdgcode)->Charge();          
          mass = pdg->GetParticle(pdgcode)->Mass();         
          //saving info for electrons and positrons
          if (TMath::Abs(charge)>0){
           energy = TMath::Sqrt(mass*mass + momentum * momentum);
           
           hE_pid->Fill(plateid, energy);
           hoccupancy->Fill(plateid);
           nelectrons[plateid-1]++;
          }
         }
     }//end of hit loop
  maxelectrons = 0;
  for(int iplate =0; iplate < nplates; iplate++){
   if (nelectrons[iplate] > maxelectrons){
     maxelectrons = nelectrons[iplate];
     maxplate = iplate;
   }
  }
  hmaxplate->Fill(maxplate+1);
  hmaxsegments->Fill(maxelectrons);
 } //end of event loop 

 hE_pid->Draw();
 TCanvas *c_occ = new TCanvas();
 hoccupancy->Scale(1./nevents);
 hoccupancy->Draw();
 
 TCanvas *cmax = new TCanvas();
 cmax->Divide(1,2);
 cmax->cd(1);
 hmaxplate->Draw();
 cmax->cd(2);
 hmaxsegments->Draw();
}
